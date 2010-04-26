import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.filter.CommonFilters import CommonFilters
import sys, math
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

import rock

class World(DirectObject):
    def __init__(self):
        self.rocks = rock.Rock("Red",self)
        self.rink = loader.loadModel("art/Rink.egg")
        self.rink.setScale(1)
        self.rink.reparentTo(render)
        
        self.keyMap = {"push":0}  

        self.accept("mouse1", self.setKey, ["push", 1])    
        self.accept("mouse1-up", self.setKey, ["push", 0])
        self.accept('escape', sys.exit)
	
        camera.setPos(10, 10, 20)
    
    def setKey(self, key, value):
        self.keyMap[key] = value
        