from direct.showbase.DirectObject import DirectObject

class Camera(DirectObject): 
    def __init__(self, world):
        self.world = world
        self.currentView = 1
        self.shotView = 1
        self.topView = 2
        self.rockView = 3
        self.followView = 4
        self.postShotView = 3
        self.shotReset = False
        
    def setCamera(self, key):
        if self.world.rocksMoving == False and (key == self.rockView or key == self.followView):
            self.postShotView = key
        else:
            self.currentView = key
            self.postShotView = key
        
    def changeView(self):
        self.currentView = self.postShotView
        
    def Update(self):
        if not self.world.rocksMoving and self.shotReset == False:
            self.currentView = self.shotView
            self.shotReset = True
        if self.world.rocksMoving:
            self.currentView = self.postShotView
            self.shotReset = False
        if self.currentView == self.shotView:
            base.camera.setPos(0,-90,20)
            base.camera.setHpr(0,-20,0)
        if self.currentView == self.topView:
            base.camera.setPos(0,29,100)
            base.camera.setHpr(180,-90,0)
        if self.currentView == self.rockView:         
            rockPos = self.world.activeRocks[-1].rock.getPos()
            base.camera.setPos(rockPos.getX(),rockPos.getY(),rockPos.getZ()+.5)
            base.camera.setHpr(self.world.activeRocks[-1].rock.getHpr())
        if self.currentView == self.followView:
            rockPos = self.world.activeRocks[-1].rock.getPos()
            rockHpr = self.world.activeRocks[-1].rock.getHpr()
            base.camera.setPos(0,self.world.activeRocks[-1].rock.getY()-30,10)
            base.camera.lookAt(0,41,0)
    
    