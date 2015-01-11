from threading import Thread
import time
import config
from viewmanagers import SlideShow, ViewManager
from curtain import Curtain
from plugins.strobe import Strobe
from plugins.rainbow import Rainbow
from plugins.snakes import Snakes
from plugins.snakes2 import Snakes as Snakes2
from plugins.ec import EC
from plugins.fancyrainbow import FancyRainbow
from plugins.sometext import SomeText
from plugins.sidescroll import SideScroll, SideScrollCreator
from plugins.wave import Wave
from plugins.beatpulse import BeatPulse
from plugins.heightlines import HeightLines
from plugins.conway import Conway
from beat_sender import beat_event_pb2
from ck import CK


bg = SlideShow(period=25)
# bg.add(EC)
bg.add(FancyRainbow)
bg.add(Wave)
bg.add(Snakes2)
# bg.add(FancyRainbow)
# bg.add(Conway)
# if config.ENABLE_BEATS:
    # bg.add(BeatPulse)
# bg.add(Snakes)
# bg.add(FancyRainbow) #REPEAT
bg.add(SideScrollCreator("Happy New Year!"))
bg.add(HeightLines)


curtain = Curtain()
# DUDE, IF YOU'RE WONDERING WHY IT'S DIM, RIGHT HERE.
vm = ViewManager(curtain=curtain, bg=bg, brightness_factor=0.7)

ck = CK()

if config.ENABLE_TWITTER:
    from twitter_client import TwitterCrawler

    def on_tweet(tweet):
        print "tweet: {}".format(tweet)
        vm.interrupt(SideScrollCreator(tweet.text.upper()))

    twc = TwitterCrawler(callback=on_tweet)
    twc.start()

if config.ENABLE_BEATS:
    from beat_sender.client import BeatReceiver

    def on_beat(beat_event):
        vm.recv_beat(beat_event)
        if beat_event.type == beat_event_pb2.COLOR:
            (r, g, b) = beat_event.r, beat_event.g, beat_event.b
            ck.set_color(0, r, g, b )
            ck.set_color(1, r, g, b )
            ck.set_color(2, r, g, b )
            ck.update()

    #br = BeatReceiver("tcp://127.0.0.1:8000", callback=on_beat)
    br = BeatReceiver("tcp://*:8001", callback=on_beat)
    br.start()


vm.start()
