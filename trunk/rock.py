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
        self.rock = loader.loadModel("art/Rock "+color+".egg")
        self.rock.setScale(.065)
        self.rock.setZ(self.rock.getZ()+.1)
        self.rock.reparentTo(render)
        self.velocity = 3
        self.friction = 0.0168
        self.mass = 18
        self.gravity = 9.81

        self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "headlight":0, "fire":0}
        taskMgr.add(self.update, "Update")

    def setkeyMap(self, keyMap):
        self.keyMap = keyMap
        

    def update(self, task):
        normalforce = self.mass * self.gravity
        frictionforce = normalforce * self.friction
        acceleration = frictionforce / self.mass
        self.velocity -= acceleration
        
        if(self.velocity > 0):
            self.rock.setPos(self.rock.getX(), self.rock.getY()+ self.velocity, self.rock.getZ())
        else:
            print "Rock stopped"
            return Task.done
            
        return Task.cont
    