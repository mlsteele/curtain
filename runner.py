from threading import Thread
import time
from twitter_client import TwitterCrawler
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
from plugins.heightlines import HeightLines


bg = SlideShow(15)
bg.add(EC)
bg.add(Wave)
bg.add(Snakes2)
bg.add(FancyRainbow)
#bg.add(Strobe)
bg.add(Snakes)
bg.add(SideScrollCreator("WELCOME TO EAST CAMPUS!"))
bg.add(HeightLines)

curtain = Curtain()
vm = ViewManager(curtain=curtain, bg=bg)

def twitter_thread():
    def on_tweet(tweet):
        print "tweet: {}".format(tweet)
        vm.interrupt(SideScrollCreator(tweet.text.upper()))

    twc = TwitterCrawler(callback=on_tweet)
    twc.start()

Thread(target=twitter_thread).start()
vm.start()
