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

class Rock(DirectObject): #use to create player tank
    def __init__(self, color, world):
        self.world = world
        self.color = color
        self.rock = loader.loadModel("art/Rock "+color+".egg")
        self.rock.setScale(1)
        self.rock.setZ(self.rock.getZ()+.7)
        self.rock.setY(self.rock.getY() - 60)
        self.rock.reparentTo(render)
        self.yvelocity = 0.750
        self.xvelocity = 0
        self.spin = 1
        self.friction = 0.0168
        self.mass = 18
        self.radius = 0.195
        self.gravity = 9.81
        self.move = False

        self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "headlight":0, "fire":0}
        
    def setkeyMap(self, keyMap):
        self.keyMap = keyMap        

    def Update(self):
        dt = globalClock.getDt()
        
        ##if self.world.keyMap["push"]:
        ##    self.move = True
    
            
        #if self.move == True:
        normalforce = self.mass * self.gravity
        frictionforce = normalforce * self.friction
        acceleration = frictionforce / self.mass
        self.yvelocity -= acceleration * dt
        self.xvelocity = self.spin * self.radius * 7 * dt
        
        if(self.yvelocity > 0):
            self.rock.setPos(self.rock.getX() + self.xvelocity, self.rock.getY()+ self.yvelocity, self.rock.getZ())
            self.rock.setH(self.rock.getH()-self.spin)
        else:
            self.yvelocity = 0
            self.xvelocity = 0
            #print "Rock stopped"
            #return Task.done
    
        #return Task.cont
    