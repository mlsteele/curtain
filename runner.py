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
from plugins.zthrough import ZThrough


bg = SlideShow(period=15)
bg.add(EC)
bg.add(Wave)
bg.add(Snakes2)
bg.add(FancyRainbow)
bg.add(Conway)
if config.ENABLE_BEATS:
    bg.add(BeatPulse)
bg.add(Snakes)
bg.add(SideScrollCreator("WELCOME TO EAST CAMPUS!"))
bg.add(HeightLines)
# bg.add(ZThrough)

curtain = Curtain()
vm = ViewManager(curtain=curtain, bg=bg)

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

    #br = BeatReceiver("tcp://127.0.0.1:8000", callback=on_beat)
    br = BeatReceiver("tcp://18.189.14.119:8000", callback=on_beat)
    br.start()


vm.start()
