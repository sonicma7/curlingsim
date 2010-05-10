from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib
from pandac.PandaModules import TextNode
from direct.gui.DirectGui import *

class HUD(object):
    def __init__(self,world):     
        self.world = world
        self.thrust = 0
        self.spin = 0
        self.yellowScore = 0
        self.redScore = 0
        self.endCount = 1
        
        self.thrustText = OnscreenText(text=("Thrust: " + str(self.thrust)),
                              style=1, fg=(0,0,1,1),
                              pos=(-1.3,0.87), scale = .07, mayChange = 1, align = TextNode.ALeft)
        self.spinText = OnscreenText(text=("Spin: " + str(self.spin)),
                              style=1, fg=(0,0,1,1),
                              pos=(-1.3,0.77), scale = .07, mayChange = 1, align = TextNode.ALeft)
                              
        self.yellowScoreText = OnscreenText(text=("Yellow Score: " + str(self.yellowScore)),
                              style=1, fg=(1,1,0,1),
                              pos=(-1.3,0.67), scale = .07, mayChange = 1, align = TextNode.ALeft)
        self.redScoreText = OnscreenText(text=("Red Score:     " + str(self.redScore)),
                              style=1, fg=(1,0,0,1),
                              pos=(-1.3,0.57), scale = .07, mayChange = 1, align = TextNode.ALeft)
        
        self.endCountText = OnscreenText(text=("End: " + str(self.endCount)),
                              style=1, fg=(0,0,1,1),
                              pos=(-1.3,0.47), scale = .07, mayChange = 1, align = TextNode.ALeft)
    
    def Update(self):
        pass
        
    def resetShot(self):
        self.thrust = 0
        self.spin = 0
        self.updateThrust(0)
        self.updateSpin(0)
        
    def updateEndCount(self):
        self.endCount += 1                                      
        self.endCountText["text"] = "End: " + str(self.endCount)
        
    def updateThrust(self, key):
        self.thrust += key
        self.thrustText["text"] = "Thrust: " + str(self.thrust)
        
    def updateSpin(self, key):
        self.spin += key
        self.spinText["text"] = "Spin: " + str(self.spin)
        
    def updateScore(self,scoreColor,score):
        if scoreColor == "Red":
            self.redScore += score
            self.redScoreText["text"] = "Red Score:     " + str(self.redScore)
        else:
            self.yellowScore += score
            self.yellowScoreText["text"] = "Yellow Score: " + str(self.yellowScore)
            
        
        
    
        
        
    '''def updateScores(self,playerScore):
        if self.world.gameover == True:
            self.playerScore.destroy()
        else:
            self.pscore += playerScore
            self.playerScore["text"] = "Current Score: " + str(self.pscore);
    
    def updateTimer(self, time):
        if self.world.gameover == True:
            self.timer.destroy()
            self.playerScore.destroy()
        else:
            currenttime = str(int(self.time - time))
            if int(currenttime) == 0: 
                self.world.gameover = True
            minutes = int(currenttime)/60
            seconds = int(currenttime)%60 
            if seconds < 10:
                seconds = "0" + str(seconds)
            if currenttime == 0: 
                self.world.gameover = True
            self.timer["text"] = "Time Remaining: " + str(minutes) + ":" + str(seconds);'''

