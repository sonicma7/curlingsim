import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
from direct.task import Task
    
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

import sys, math, os, random
import world

from pandac.PandaModules import Filename

class Broom(DirectObject):
    def __init__(self, world):
        self.world = world
        self.broom1 = loader.loadModel("art/Broom.egg")
        self.broom2 = loader.loadModel("art/Broom.egg")
        self.broom1.setZ(self.broom1.getZ()+.7)
        self.broom1.setH(self.broom1.getH()+90)
        self.broom2.setZ(self.broom2.getZ()+.7)
        self.broom2.setH(self.broom2.getH()-90)
        self.broom1.reparentTo(render)
        self.broom2.reparentTo(render)
        
        self.broom1Offset = [.1,.2,.3,.4,.5,.4,.3,.2,.1,.0,-.1,-.2,-.3,-.4,-.5,-.4,-.3,-.2,-.1,0]
        self.broom1OffsetPos = 0
        self.broom2Offset = [-.1,-.2,-.3,-.4,-.5,-.4,-.3,-.2,-.1,.0,.1,.2,.3,.4,.5,.4,.3,.2,.1,0]
        self.broom2OffsetPos = 0
        
        self.sweep = False
        
    def setSweep(self,key):
        self.sweep = key

        
    def Update(self):
        try: 
            rockPos = self.world.activeRocks[-1].rock.getPos()
            rock = self.world.activeRocks[-1] 
        except: 
            rockPos = self.world.currentRock.rock.getPos()
            rock = self.world.currentRock
        self.broom1.setY(rockPos.getY()+1)   
        self.broom1.setX(rockPos.getX())             
        self.broom2.setY(rockPos.getY()+1.5)
        self.broom2.setX(rockPos.getX())
        if self.sweep:
            rock.friction = .014 
            self.broom1.setX(self.broom1.getX()+self.broom1Offset[self.broom1OffsetPos])
            self.broom2.setX(self.broom2.getX()+self.broom2Offset[self.broom2OffsetPos])
            self.broom1OffsetPos += 1
            self.broom2OffsetPos += 1
            if self.broom1OffsetPos >= len(self.broom1Offset):
                self.broom1OffsetPos = 0
                self.broom2OffsetPos = 0
        else:
            rock.friction = .0168
            self.broom1.setX(self.broom1.getX()+self.broom1Offset[self.broom1OffsetPos])
            self.broom2.setX(self.broom2.getX()+self.broom2Offset[self.broom2OffsetPos])    
        
            
            