import zmq, threading, time
import beat_event_pb2


class BeatBlaster(object):
    

    def __init__(self, audience = None):

        self.audience = audience

        self.ctx = zmq.Context()
        self.publisher = self.ctx.socket(zmq.PUB)

        if self.audience:
            self.publisher.bind(audience)
        else:
            self.publisher.bind("tcp://*:8000")

        time.sleep(1)

    def beat(self, bar):
        beat_event = beat_event_pb2.BeatEvent()
        beat_event.bar = bar
        beat_event.sub_bar = 0
        self.publisher.send_multipart(['bar', beat_event.SerializeToString()])

    def sub_beat(self, bar, sub_bar):
        beat_event = beat_event_pb2.BeatEvent()
        beat_event.bar = bar
        beat_event.sub_bar = sub_bar
        self.publisher.send_multipart(['sub_bar', beat_event.SerializeToString()])
    def close(self):
        pass
                         


if __name__ == '__main__':
    try:
        n = BeatBlaster("tcp://*:8000")
        while True:
            n.beat(1 ) 
            n.sub_beat(1, 5 ) 
            print "sent"
            
            time.sleep(1)
    except KeyboardInterrupt:
        print "Exiting"
        n.close()


