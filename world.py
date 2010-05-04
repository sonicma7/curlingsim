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

import rock, camera

class World(DirectObject):
    def __init__(self):
        self.camera = camera.Camera(self)
        self.currentRock = rock.Rock("Red",self)        
        self.activeRocks = []       
        self.rink = loader.loadModel("art/Rink.egg")
        self.rink.setScale(1)
        self.rink.reparentTo(render)
        self.turn = 1
        
        self.rocksMoving = False
        
        self.keyMap = {"push":0}  

        self.accept("k", self.pushRock)    
        #self.accept("k-up", self.setKey, ["push", 0])
        self.accept('escape', sys.exit)
        self.accept("1", self.camera.setCamera,[1])
        self.accept("2", self.camera.setCamera,[2])
        self.accept("3", self.camera.setCamera,[3]) 
        self.accept("4", self.camera.setCamera,[4])
        
        taskMgr.add(self.update, "World-Update")

    
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def pushRock(self):
        self.activeRocks.append(self.currentRock)
        if self.currentRock.color == "Red":
            self.currentRock = rock.Rock("Yellow",self)
        else:    
            self.currentRock = rock.Rock("Red",self)
        #self.camera.changeView()
        
    def update(self, task):
        self.rocksMoving = False         
        for i in self.activeRocks:
            i.Update()
            if i.xvelocity != 0 or i.yvelocity != 0:
                self.rocksMoving = True
        self.checkCollisions()
        self.camera.Update()
        return task.cont
        
    def checkCollisions(self):
        for i in self.activeRocks:
            for j in self.activeRocks:
                if i != j:
                    ax = i.rock.getPos().getX()
                    ay = i.rock.getPos().getY()
                    az = i.rock.getPos().getZ()
                    bx = j.rock.getPos().getX()
                    by = j.rock.getPos().getY()
                    bz = j.rock.getPos().getZ()
                    dx = ax-bx
                    dy = ay-by
                    dz = az-bz
                    distance = math.sqrt(dx*dx+dy*dy+dz*dz)
                    if distance < 2*i.radius: 
                        velocity = i.yvelocity + j.yvelocity
                        i.yvelocity = velocity/2
                        j.yvelocity = velocity/2
                        
    def computeDistance(a,b):
        pass