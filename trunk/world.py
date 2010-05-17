#Copyright Mark Aversa, Jeremy Therrien
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


#ID generator for the curling rocks.  Used with collision checking.
def id_gen():
    k = 0
    while True:
        k += 1
        yield k

unique_id = id_gen().next


class World(DirectObject):
    """The world that holds the rocks, brooms, and rink.  The game is updated through
    this class and it handles collisions, throwing of the rock, and aiming of the rock."""
    def __init__(self):        
        self.turn = 0
        self.camera = camera.Camera(self)
        self.hud = hud.HUD(self)
        self.sweepingBrooms = broom.Broom(self)
        self.aimBroom = broom.AimBroom(self)
        id = str(unique_id())
        self.preload = rock.Rock("Yellow",id,self)
        self.preload.rock.removeNode()
        del self.preload 
        self.currentRock = rock.Rock("Red", id, self)
        self.lastEndColor = "Red"        
        self.activeRocks = []       
        self.rink = loader.loadModel("art/Rink.egg")
        self.rink.setScale(1)
        self.rink.reparentTo(render)
        self.end = 1
        self.endsToPlay = 8
        
        self.rocksMoving = False
        
        self.keyMap = {"push":0}  

        self.accept("space", self.pushRock)    
        #self.accept("k-up", self.setKey, ["push", 0])
        self.accept('escape', sys.exit)
        self.accept("1", self.camera.setCamera,[1])
        self.accept("2", self.camera.setCamera,[2])
        self.accept("3", self.camera.setCamera,[3]) 
        self.accept("4", self.camera.setCamera,[4]) 
        self.accept("9", self.camera.setCamera,[9])  
        self.accept("d", self.setDebugging)
        self.accept("arrow_up", self.hud.updateWeight,[1]) 
        self.accept("arrow_down", self.hud.updateWeight,[-1])        
        self.accept("arrow_right", self.hud.updateSpin,[1]) 
        self.accept("arrow_left", self.hud.updateSpin,[-1])
        self.accept("mouse1", self.determineMouseAction,[True])
        self.accept("mouse1-up", self.determineMouseAction,[False])
        
        taskMgr.add(self.update, "World-Update")
        
        self.debugging = True #Set to true so some gameplay features are modified for testing (or other fun things)
        
        self.gameOver = False
        

    #Input
    def setKey(self, key, value):
        self.keyMap[key] = value
     
    #Debugging mode
    def setDebugging(self):
        if self.debugging == True:
            self.debugging = False
        else:
            self.debugging = True
    
    #calculates the velocity of the rock 
    def calculateVelocity(self): #Calculates the Vec3 velocity of the stone
        if self.aimBroom.aimed == False:
            broomPos = Vec3(0,57,.7)
        else:
            broomPos = self.aimBroom.broom.getPos()
        velocity = broomPos-self.currentRock.rock.getPos()
        velocity.normalize()
        velocity.setY(velocity.getY()*.7 + (self.hud.weight *.01))
        return velocity
        
    #Used for input of the mouse to determine throwing angle   
    def determineMouseAction(self,key):
        if self.gameOver == True:
            return
        if self.turn == 16 and self.rocksMoving == False:
            self.turn = 0
            self.hud.updateTurn()
            self.end += 1
            self.hud.updateEndCount()
            #if self.end >= self.endsToPlay + 1 and self.hud.yellowScore != self.hud.redScore:
            #    self.gameOver = True
            #    self.end -= 1
            #    self.camera.setCamera(3)
            #    return
            if self.activeRocks == []: #Blank End
                #print "Blank end"
                self.currentRock = rock.Rock(self.lastEndColor, id, self)                 
            elif self.lastEndColor == "Yellow":                
                self.currentRock = rock.Rock("Red", id, self)
                self.lastEndColor = "Red"
            else:
                self.currentRock = rock.Rock("Yellow", id, self)
                self.lastEndColor = "Yellow"
            self.clearRocks()
            self.camera.setCamera(1)
            return
        if self.rocksMoving:      
            self.sweepingBrooms.setSweep(key)
        else:
            self.sweepingBrooms.setSweep(False)
            
        if key == True and self.rocksMoving == False and (self.camera.currentView == self.camera.topView or self.camera.currentView == self.camera.topCloseView):
            if self.aimBroom.aimed == False:
                self.aimBroom.aimed = True
            elif self.aimBroom.aimed == True:
                self.aimBroom.aimed = False
    
    #Starts movement of the rock
    def pushRock(self):                         
        #if self.aimBroom.aimed == True:
        if self.turn != 16 and (self.rocksMoving == False or self.debugging == True):
            id = str(unique_id()) 
            self.turn += 1
            self.hud.updateTurn()
            self.rocksMoving = True           
            self.currentRock.spin = self.hud.spin*.5
            self.currentRock.velocity = self.calculateVelocity()
            self.aimBroom.aimed = False
            self.hud.resetShot()
            self.activeRocks.append(self.currentRock)
            self.sweepingBrooms.sweepingRock = self.activeRocks[-1]
            if self.turn != 16:
                if self.currentRock.color == "Red":
                    self.currentRock = rock.Rock("Yellow", id, self)
                else:    
                    self.currentRock = rock.Rock("Red", id, self)
            #self.camera.changeView()
            for i in self.activeRocks:
                i.collideDict[self.currentRock.id] = False
                self.currentRock.collideDict[i.id] = False
                
    #Calculates scores at the end of the round            
    def calculateScores(self):
        for i in self.activeRocks:
            i.distanceToButton = self.computeDistanceToButton(i)
        self.activeRocks = sorted(self.activeRocks,self.sortByDistance)
        score = 0
        scoreColor = self.activeRocks[0].color
        for i in self.activeRocks:
            if i.color == scoreColor and i.distanceToButton <= 6.35:
                score += 1
            else:
                break
        self.hud.updateScore(scoreColor,score)
            
    #Sorts the rocks based on their distance
    def sortByDistance(self,a,b):
        if a.distanceToButton > b.distanceToButton:
            return 1
        return -1
      
    #Update function, called every frame to update rocks, friction, brooms, and collisions
    def update(self, task):
        self.camera.Update()
        if self.gameOver == True:
            pass
        elif self.turn == 16 and self.rocksMoving == False:
            self.camera.setCamera(3)
            self.aimBroom.hideBroom()
            self.sweepingBrooms.hideBroom()
            if self.activeRocks != []:
                if self.activeRocks[0].distanceToButton == 100:
                    self.calculateScores()
            if self.end >= self.endsToPlay and self.hud.yellowScore != self.hud.redScore:
                self.gameOver = True
                self.end -= 1
        else:
            self.rocksMoving = False         
            for i in self.activeRocks:
                i.Update()
                if i.velocity.getX() != 0 or i.velocity.getY() != 0:
                    self.rocksMoving = True
            self.checkCollisions()
            self.sweepingBrooms.Update()
            self.aimBroom.update()                   
            self.removeOutofBoundsRocks()
        self.hud.Update()
        return task.cont
        
    #removes the rocks that out of bounds of the rink
    def removeOutofBoundsRocks(self):
        delete = []
        for i in xrange(len(self.activeRocks)):                                                                                                                                                                        
            if self.activeRocks[i].rock.getX() > 7.28 or self.activeRocks[i].rock.getX() < -7.28 or self.activeRocks[i].rock.getY() > 63.48 or (self.rocksMoving == False and self.activeRocks[i].rock.getY() < 36.6):
                delete.append(i)
        for i in xrange(len(delete)):
            #print delete,self.activeRocks
            self.activeRocks[delete[i]-i].rock.removeNode()
            self.activeRocks.pop(delete[i]-i)
    
    #Clears rocks at the end of the round
    def clearRocks(self):
        for i in xrange(len(self.activeRocks)):
            self.activeRocks[0].rock.removeNode()
            self.activeRocks.pop(0)
    
    #checks for collisions between two rocks
    def checkCollisions(self):
        for i in self.activeRocks:
            for j in self.activeRocks:
                if i != j:
                    if self.computeDistance(i,j) < 2*i.radius: 
                        if i.collideDict[j.id] == False:
                            j.collideDict[i.id] = True
                            self.separateRocks(i, j)
                            self.computeRotation(i, j)
                            self.computeCollision(i, j)

                    else:
                        if i.collideDict[j.id] == True:
                            i.collideDict[j.id] = False
    
    #Finds the normal between two points
    def findNormal(self, a,b):
        return Vec3(b.rock.getPos().getX()-a.rock.getPos().getX(), b.rock.getPos().getY()-a.rock.getPos().getY(),0)
    
    #Computes the unit value of the given vector
    def getUnitNormal(self, normal):
        return normal/(math.sqrt(pow(normal.getX(),2) + pow(normal.getY(),2)))
    
    #Computes the distance between two rocks
    def computeDistance(self, a,b):
        ax = a.rock.getPos().getX()
        ay = a.rock.getPos().getY()
        bx = b.rock.getPos().getX()
        by = b.rock.getPos().getY()
        dx = ax-bx
        dy = ay-by
        return math.sqrt(dx*dx+dy*dy)
    
    #Computes the distance a rock is from the center
    def computeDistanceToButton(self, a):
        ax = a.rock.getPos().getX()
        ay = a.rock.getPos().getY()
        bx = 0
        by = 57
        dx = ax-bx
        dy = ay-by
        return math.sqrt(dx*dx+dy*dy)
        
    #Computes the scalar value of a vector
    def computeScalar(self, a):
        return math.sqrt(pow(a.getX(),2) + pow(a.getY(),2))
    
    #Computes the new forces given each rock after they collide
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
    
    #Separates the rocks so they do not stick together after a collision
    def separateRocks(self, i, j):
        normal = self.findNormal(i, j)
        unitnormal = self.getUnitNormal(normal)
        distance = self.computeDistance(i, j)
        move = (2*i.radius - distance)
        i.rock.setX(i.rock.getX() - (unitnormal.getX() * (move/distance)))
        i.rock.setY(i.rock.getY() - (unitnormal.getY() * (move/distance)))
    
    #computes the new rotation of each rock after a collision
    def computeRotation(self, i, j):
        if i.velocity.getY() > 0 or i.velocity.getY() < 0:
            direction = i.velocity * -1
            unitdir = self.getUnitNormal(direction)
            force = i.velocity * i.mass
            normal = self.findNormal(i, j)
            unitnormal = self.getUnitNormal(normal)
            collision = unitnormal.dot(unitdir)
            if(collision > 1 or collision < -1):
                return
            if(collision == -1 or collision == 1):
                collision = -1
            angle = math.acos(collision)
            torque = force * i.radius * math.sin(angle)
            scalartorque = self.computeScalar(torque)
            i.spin = i.spin - (scalartorque/2)
            j.spin = scalartorque/2
             
        else:
            direction = j.velocity * -1
            unitdir = self.getUnitNormal(direction)
            force = j.velocity * j.mass
            normal = self.findNormal(j, i)
            unitnormal = self.getUnitNormal(normal)
            collision = unitnormal.dot(unitdir)
            if(collision > 1 or collision < -1):
                return
            if(collision == -1 or collision == 1):
                collision = -1
            angle = math.acos(collision)
            torque = force * j.radius * math.sin(angle)
            scalartorque = self.computeScalar(torque)
            j.spin = j.spin - (scalartorque/2)
            i.spin = scalartorque/2

            