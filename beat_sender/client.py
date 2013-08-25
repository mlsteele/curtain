import zmq, time, threading
import beat_event_pb2

class BeatReceiver(threading.Thread):

    def __init__(self, sub = None,
                 beats = True,
                 sub_beats = False,
                 change_scene = False,
                 color = False,
                 callback = False):

        self.callback = callback
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.ctx = zmq.Context()
        self.sub = self.ctx.socket(zmq.SUB)

        if beats:
            self.sub.setsockopt(zmq.SUBSCRIBE, 'b')
        if sub_beats:
            self.sub.setsockopt(zmq.SUBSCRIBE, 's')
        if change_scene:
            self.sub.setsockopt(zmq.SUBSCRIBE, 'c')
        if color:
            self.sub.setsockopt(zmq.SUBSCRIBE, 'C')
        if sub:
            self.sub.bind(sub)
	    print "BeatReceiver binded to %s " % sub
        else:
            self.sub.bind("tcp://127.0.0.1:8001")
            print "BeatReceiver binded."

        time.sleep(1)


    def run(self):
        self.running = True
        beat_event = beat_event_pb2.BeatEvent()
        print "BeatReceiver running."
        while self.running:
            tag, message = self.sub.recv_multipart()
            beat_event.ParseFromString(message)

            if self.callback:
                self.callback(beat_event)
            else:
                if beat_event.type == beat_event_pb2.BEAT:
                    print "Beat"
                elif beat_event.type == beat_event_pb2.COLOR:
                    print "COLOR", str((beat_event.r, beat_event.g,
                                        beat_event.b))



if __name__ == '__main__':
    n = BeatReceiver("tcp://127.0.0.1:8001", sub_beats = True, color =True)
    n.start()

    time.sleep(10)
