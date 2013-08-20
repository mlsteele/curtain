import zmq, time, threading
import beat_event_pb2

class BeatReceiver(threading.Thread):
    
    def __init__(self, sub = None, 
                 beats = True, 
                 sub_beats = False,
                 callback = False):

        self.callback = callback
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.ctx = zmq.Context()
        self.sub = self.ctx.socket(zmq.SUB)

        self.sub.setsockopt(zmq.SUBSCRIBE, 'bar')
        self.sub.setsockopt(zmq.SUBSCRIBE, 'sub_bar')
        if sub:
            self.sub.connect(sub)
        else:
            self.sub.connect("tcp://127.0.0.1:8000")
            print "Connected"

        time.sleep(1)


    def run(self):
        self.running = True
        beat_event = beat_event_pb2.BeatEvent()
        print "Running "
        while self.running:
            tag, message = self.sub.recv_multipart()
            beat_event.ParseFromString(message)

            if self.callback:
                self.callback(beat_event)
            else:
                print beat_event




if __name__ == '__main__':
    n = BeatReceiver()
    n.start()

    time.sleep(10)
