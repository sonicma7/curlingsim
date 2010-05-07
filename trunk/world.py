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

import rock, camera, hud, broom

def id_gen():
    k = 0
    while True:
        k += 1
        yield k

unique_id = id_gen().next

class World(DirectObject):
    def __init__(self):
        self.camera = camera.Camera(self)
        self.hud = hud.HUD(self)
        self.sweepingBrooms = broom.Broom(self)
        id = str(unique_id())
        self.currentRock = rock.Rock("Red", id, self)        
        self.activeRocks = []       
        self.rink = loader.loadModel("art/Rink.egg")
        self.rink.setScale(1)
        self.rink.reparentTo(render)
        self.turn = 0
        
        self.rocksMoving = False
        
        self.keyMap = {"push":0}  

        self.accept("k", self.pushRock)    
        #self.accept("k-up", self.setKey, ["push", 0])
        self.accept('escape', sys.exit)
        self.accept("1", self.camera.setCamera,[1])
        self.accept("2", self.camera.setCamera,[2])
        self.accept("3", self.camera.setCamera,[3]) 
        self.accept("4", self.camera.setCamera,[4]) 
        self.accept("9", self.camera.setCamera,[9])
        self.accept("arrow_up", self.hud.updateThrust,[1]) 
        self.accept("arrow_down", self.hud.updateThrust,[-1])        
        self.accept("arrow_right", self.hud.updateSpin,[1]) 
        self.accept("arrow_left", self.hud.updateSpin,[-1])
        self.accept("mouse1", self.sweepingBrooms.setSweep,[True])
        self.accept("mouse1-up", self.sweepingBrooms.setSweep,[False])
        
        taskMgr.add(self.update, "World-Update")

    
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def calculateVelocity(self): #Calculates the Vec3 velocity of the stone
        return Vec3(0,self.hud.thrust*.01,0) +self.currentRock.velocity
            
    def pushRock(self):
        id = str(unique_id()) 
        self.turn += 1                  
        self.currentRock.spin = self.hud.spin*.5
        self.currentRock.velocity = self.calculateVelocity()
        self.activeRocks.append(self.currentRock)
        if self.currentRock.color == "Red":
            self.currentRock = rock.Rock("Yellow", id, self)
        else:    
            self.currentRock = rock.Rock("Red", id, self)
        #self.camera.changeView()
        for i in self.activeRocks:
            i.collideDict[self.currentRock.id] = False
            self.currentRock.collideDict[i.id] = False
        if self.turn == 16:
            print "UPDATE SCORES"
        
    def update(self, task):
        if self.turn == 16 and self.rocksMoving == False:
            self.camera.setCamera(5)
        else:
            self.rocksMoving = False         
            for i in self.activeRocks:
                i.Update()
                if i.velocity.getX() != 0 or i.velocity.getY() != 0:
                    self.rocksMoving = True
        self.checkCollisions()
        self.camera.Update()
        self.sweepingBrooms.Update()
        self.removeOutofBoundsRocks()
        self.hud.Update()
        return task.cont
        
    def removeOutofBoundsRocks(self):
        delete = []
        for i in xrange(len(self.activeRocks)):
            if self.activeRocks[i].rock.getX() > 11.857 or self.activeRocks[i].rock.getX() < -11.857 or self.activeRocks[i].rock.getY() > 65:
                delete.append(i)
        for i in xrange(len(delete)):
            #print delete,self.activeRocks
            self.activeRocks[delete[i]-i].rock.removeNode()
            self.activeRocks.pop(delete[i]-i)
        
    def checkCollisions(self):
        for i in self.activeRocks:
            for j in self.activeRocks:
                if i != j:
                    if self.computeDistance(i,j) < 2*i.radius: 
                        if i.collideDict[j.id] == False:
                            j.collideDict[i.id] = True
                            self.separateRocks(i, j)
                            self.computeCollision(i, j);

                    else:
                        if i.collideDict[j.id] == True:
                            i.collideDict[j.id] = False
                        
    def findNormal(self, a,b):
        return Vec3(b.rock.getPos().getX()-a.rock.getPos().getX(), b.rock.getPos().getY()-a.rock.getPos().getY(),0)
    
    def getUnitNormal(self, normal):
        return normal/(math.sqrt(pow(normal.getX(),2) + pow(normal.getY(),2)))
    
    def computeDistance(self, a,b):
        ax = a.rock.getPos().getX()
        ay = a.rock.getPos().getY()
        bx = b.rock.getPos().getX()
        by = b.rock.getPos().getY()
        dx = ax-bx
        dy = ay-by
        return math.sqrt(dx*dx+dy*dy)
        
    def computeCollision(self, i, j):
        normal = self.findNormal(i, j)
        unitnormal = self.getUnitNormal(normal)
        unittangent = Vec3(-unitnormal.getY(), unitnormal.getX(), 0)
        normvelo1 = unitnormal.dot(i.velocity)
        normvelo2 = unitnormal.dot(j.velocity) 
        tangvelo1 = unittangent.dot(i.velocity)
        tangvelo2 = unittangent.dot(j.velocity)
        newnorm1 = (2 * j.mass * normvelo2)/(i.mass + j.mass)
        newnorm2 = (2 * i.mass * normvelo1)/(i.mass + j.mass)
        newnormvec1 = unitnormal * newnorm1 
        newnormvec2 = unitnormal * newnorm2
        newtangvec1 = unittangent * tangvelo1
        newtangvec2 = unittangent * tangvelo2
        i.velocity = newnormvec1 + newtangvec1
        j.velocity = newnormvec2 + newtangvec2
        
    def separateRocks(self, i, j):
        normal = self.findNormal(i, j)
        unitnormal = self.getUnitNormal(normal)
        distance = self.computeDistance(i, j)
        move = (2*i.radius - distance)
        i.rock.setX(i.rock.getX() - (unitnormal.getX() * (move/distance)))
        i.rock.setY(i.rock.getY() - (unitnormal.getY() * (move/distance)))
        