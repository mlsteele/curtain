#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <fftw3.h>
#include <math.h>

#include <jack/jack.h>

#include <zmq.h>

jack_port_t *input_port;
jack_port_t *output_port;

// For now, hardcode. Should be retreived from jack
#define N (256)
#define NBUCKETS 16
#define RESOLUTION 8
#define AVERAGE_LENGTH 20

fftw_complex *fft_out;
double *fft_in;
fftw_plan p, ifft;

double samples[N];
int bucket_max[NBUCKETS];
double buckets[NBUCKETS];

signed char data[NBUCKETS];
signed char old_data[NBUCKETS];
signed char d_data[NBUCKETS];
signed char old_d_data[NBUCKETS];
signed char d2_data[NBUCKETS];

signed char d_average[NBUCKETS];


void my_free(void * data, void *hint) {
    free(data);
}

//zeromq stuff

void *socket;  
zmq_msg_t  msg;
#define ENDPOINT "tcp://*:8001"

void init_fft() {
    fft_in = (double*) fftw_malloc(sizeof(double) * N);
    fft_out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
    // make the inverse transform
    p = fftw_plan_dft_r2c_1d(N, fft_in, fft_out, 0);
    //ifft = fftw_plan_dft_c2r_1d(N, fft_out, fft_in, 0);
}

void destroy_fft(void) {
    fftw_destroy_plan(p);
    fftw_free(fft_in); fftw_free(fft_out);
}

int sum(char * data, int len){
    int sum = 0;
    for(int i = 0; i < len; i ++) {
        sum += data[i];
    }
    return sum;
}

void running_average(char * bucket, char value, int length) {
    double avg = (double) *bucket;
    avg = (avg * (double) length) / (double) value;
    *bucket = (char) avg;
}
void average_buckets(double * samples, double * buckets, int nsamples, int nbuckets) {

    int bucket_width = (nsamples / 2 +1 )  / nbuckets;
    int bucket, sample = 0;
    for (bucket = 0; bucket < nbuckets; bucket++) {
        for (int i = 0; i < bucket_width; i++) {
            sample++;
            if ( bucket < nbuckets && sample < nsamples){
                buckets[bucket]  += abs(samples[sample]);
            } else {
                break; 
            }
        }
        buckets[bucket] /=  (double) bucket_width;
    }
    for (int i = 0; i < NBUCKETS; i ++) {
        int value  = (int) buckets[i];
        if ( fabs(value) > bucket_max[i]){
            bucket_max[i] = fabs(value);
        }

        if (bucket_max[i] != 0) {
            data[i] =  (value * RESOLUTION) / bucket_max[i];
        } else {
            data[i] =  value;
        }
        //calculate 1st and 2nd deriviatives
        d_data[i] = data[i] - old_data[i];
        d2_data[i] = d_data[i] - old_d_data[i];

        old_d_data[i]  = d_data[i];
        old_data[i] = data[i];

        running_average(&d_average[0], sum(d_data, NBUCKETS), i);

        for (int j = 0; j < d_data[i]; j++){
            if (j > 6)
                break;
            printf("#") ;
        }
        printf("\t");



    }

    if (sum(d2_data, NBUCKETS) > 15) {
        printf("\t\t\t\t***************************************************\n") ;
    }
    printf("\n");
    
    zmq_send(socket, d_data, NBUCKETS, 0);
}


void do_fft() {
    fftw_execute(p); /* repeat as needed */

    for(int i = 0; i < N/ 2 + 1;i ++) {
        samples[i] = fft_out[i][0];
    }
    
    average_buckets(samples, buckets, N, NBUCKETS);
}

int process (jack_nframes_t nframes, void *arg)

{
	jack_default_audio_sample_t *out = (jack_default_audio_sample_t *) jack_port_get_buffer (output_port, nframes);
	jack_default_audio_sample_t *in = (jack_default_audio_sample_t *) jack_port_get_buffer (input_port, nframes);

    //copy into correct format
    for(int i=0; i < nframes; i++){
        fft_in[i] = (double) in[i];
    }
    do_fft();
	memcpy (out, in, sizeof (jack_default_audio_sample_t) * nframes);

	return 0;      
}

int main (int argc, char *argv[])
{
    init_fft();
	jack_client_t *client;
	const char **ports;


    void * zmq = zmq_init(1);

    socket = zmq_socket(zmq, ZMQ_PUB);
    int hwm = 10;
    int rc;

    while ((rc = zmq_bind(socket, ENDPOINT)) != 0) {
        printf("Pusher waiting to connect %d\n", rc) ;
        sleep(1);
    }
    printf("Bound to %s\n", ENDPOINT);


    /*
	if (argc < 2) {
		fprintf (stderr, "usage: jack_simple_client <name>\n");
		return 1;
	}
    */

	/* try to become a client of the JACK server */

	if ((client = jack_client_open ("asdf", 0, 0)) == 0) {
		fprintf (stderr, "jack server not running?\n");
		return 1;
	}

	/* tell the JACK server to call `process()' whenever
	   there is work to be done.
	*/

	jack_set_process_callback (client, process, 0);

	/* create two ports */

	input_port = jack_port_register (client, "input", JACK_DEFAULT_AUDIO_TYPE, JackPortIsInput, 0);
	output_port = jack_port_register (client, "output", JACK_DEFAULT_AUDIO_TYPE, JackPortIsOutput, 0);

	/* tell the JACK server that we are ready to roll */

	if (jack_activate (client)) {
		fprintf (stderr, "cannot activate client");
		return 1;
	}

	/* connect the ports. Note: you can't do this before the
	   client is activated, because we can't allow connections to
	   be made to clients that aren't running.

	   we want to connect to the first two "physical" input &
	   output ports, which will likely be the first two channels
	   of an audio interface (if there is one).
	*/

	if ((ports = jack_get_ports (client, NULL, NULL, JackPortIsPhysical|JackPortIsOutput)) == NULL) {
		fprintf(stderr, "Cannot find any physical capture ports");
		exit(1);
	}

	if (jack_connect (client, ports[0], jack_port_name (input_port))) {
		fprintf (stderr, "cannot connect input ports\n");
	}

	free (ports);
	
	if ((ports = jack_get_ports (client, NULL, NULL, JackPortIsPhysical|JackPortIsInput)) == NULL) {
		fprintf(stderr, "Cannot find any physical playback ports");
		exit(1);
	}

	if (jack_connect (client, jack_port_name (output_port), ports[0])) {
		fprintf (stderr, "cannot connect output ports\n");
	}

	free (ports);

	/* Since this is just a toy, run for a few seconds, then finish */
    
    while ( 1) {
        sleep (1);
    }
	jack_client_close (client);
    destroy_fft();


	exit (0);
}


