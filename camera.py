from direct.showbase.DirectObject import DirectObject

class Camera(DirectObject): 
    def __init__(self, world):
        '''Camera for the game. Commented out code is for use if you want
        specific cameras to be used before or after a shot has been taken'''
        self.world = world
        self.currentView = 1
        self.shotView = 1
        self.topView = 2
        self.rockView = 9
        self.followView = 4   
        self.topCloseView = 3
        self.postShotView = 4
        self.shotReset = False
        self.timerStarted = False
        
    def setCamera(self, key):
        #if self.world.rocksMoving == False and (key == self.rockView or key == self.followView):
        #    self.postShotView = key
        #else:
        #    self.currentView = key
        #    self.postShotView = key
        self.currentView = key 
        
    def changeView(self):
        #self.currentView = self.postShotView
        pass
        
    def Update(self):
        #if not self.world.rocksMoving and self.shotReset == False:
        #    self.currentView = self.shotView
        #    self.shotReset = True
        #if self.world.rocksMoving:
        #    self.currentView = self.postShotView
        #    self.shotReset = False
        if self.currentView == self.shotView:
            base.camera.setPos(0,-90,20)
            base.camera.setHpr(0,-20,0)
        if self.currentView == self.topView:
            base.camera.setPos(0,29,100)
            base.camera.setHpr(180,-90,0)
        if self.currentView == self.rockView:
            try: 
                rockPos = self.world.activeRocks[-1].rock.getPos()
                rockHpr = self.world.activeRocks[-1].rock.getHpr()
            except: 
                rockPos = self.world.currentRock.rock.getPos()
                rockHpr = self.world.currentRock.rock.getHpr()
            base.camera.setPos(rockPos.getX(),rockPos.getY(),rockPos.getZ()+.5)
            base.camera.setHpr(rockHpr)
        if self.currentView == self.followView:
            try: 
                rockPos = self.world.activeRocks[-1].rock.getPos()
                rockHpr = self.world.activeRocks[-1].rock.getHpr()
            except: 
                rockPos = self.world.currentRock.rock.getPos()
                rockHpr = self.world.currentRock.rock.getHpr()
            base.camera.setPos(0,rockPos.getY()-30,10)
            base.camera.lookAt(rockPos) 
        if self.currentView == self.topCloseView:
            base.camera.setPos(0,41,50)
            base.camera.setHpr(180,-90,0)
    
    