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
bg.add(SideScrollCreator("WORLD"))

curtain = Curtain()
vm = ViewManager(curtain=curtain, bg=bg)
# vm.interrupt(SideScrollCreator(tweet.text.upper()))
vm.start()
