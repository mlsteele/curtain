import pygame.midi as midi
import time
import threading
import sys

class MidiInput(threading.Thread):
    callbacks = {}
    def __init__(self,midi_id=1):
        threading.Thread.__init__(self)
        midi.init()
	self.input = midi.Input(midi_id)
    def __del__(self):
        if midi:
            midi.quit()

    def stop(self):
        print "MidiInput.stop() called"
        self.running = False

    def attach_callback(self,knob,function):
        self.callbacks[knob] = function

    def attach_kill_callback(self,function):
        self.kill_callback = function

    def run(self):
        self.running = True
        self.isAlive = True
        try:
            while True:
                if not self.running:
                    break
                while self.input.poll():
                    packet = self.input.read(1)
                    status = packet[0][0][0]
                    knob = packet[0][0][1]
                    value = packet[0][0][2]
                    print knob
                    if status==144:
                        pass
                        #self.kill_callback()

                    print "Knob: %d Value: %d , Status: %d" % (knob,value,status)
                    if knob in self.callbacks:
                        self.callbacks[knob](value)
                time.sleep(.01)
        except KeyboardInterrupt as e:
            print "MidiInput caught interrupt"
            threading.interrupt_main()
        print "Input threading quitting"
        self.isAlive = False
        midi.quit()
        sys.exit(0)

def show_value(value):
    print value

if __name__ == '__main__':
    m = MidiInput(9) 
    m.attach_callback(17,show_value)

    m.start()

    try: 
        while True:
            time.sleep(1)
    except KeyboardInterrupt as e:
        m.stop()
        while m.isAlive:
            pass
        print "input thread reports geing dead"
        sys.exit(0)



