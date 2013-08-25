import collections, threading, time, functools
from server import BeatBlaster



class BeatRepeater(threading.Thread):

    def __init__(self, callback = None, buffer_len = 3):
        self.callback = callback

        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.buffer = collections.deque(maxlen = buffer_len)
        self.now = time.time()
        self.prev = self.now
        self.delta = 0

        self.running = False

    def average(self):
	if len(self.buffer) > 1:
		indexes = [(i+1, i) for i in range(len(self.buffer) - 1)]
		deltas = [self.buffer[i+1] - self.buffer[i] for i in range(len(self.buffer) - 1)]
		self.delta = sum(deltas) / len(deltas)
	
	
    def calculated_delta(self):
        return time.time() - self.prev
    def beat(self):
        if not self.running:
            self.start()
        self.buffer.append(time.time())

        self.average()
    def output_beat(self):
        if self.callback:
            self.callback()
        else:
            print "BEAT"
            #print self.delta
    def run(self):
        self.running = True
        self.output_beat()
        while self.running:
            if self.delta > .005:
                time.sleep(self.delta)
		print "BEAT"
                self.output_beat()
            else:
		print "OMG"
                time.sleep(.005)
                
                
    def stop(self):
        self.running = False
        return self.join()

if __name__ == '__main__':
    
    try:
  
            
	publisher = BeatBlaster()
        b = BeatRepeater(functools.partial(publisher.beat, 1))        
        b.start()
        while True:
            a = raw_input("Enter on Beat: ")
            b.beat()
    except KeyboardInterrupt:
	print "Everything broke"
        b.stop()

        


    


    

