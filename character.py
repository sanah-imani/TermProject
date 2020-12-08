#player class
class Player:
    def __init__(self):
        self.frames_r = ["stickman/stick-R1.gif",
                         "stickman/stick-R2.gif",
                         "stickman/stick-R3.gif",
                         "stickman/stick-R4.gif"]
        (self.playerWidth, self.playerHeight) = (40,40)
        self.currFrame = 0
        self.currLevel = 1
        self.levelsCompleted = []
        self.stars = 0
        self.score = 0
        self.spikes = 0
        self.TNTs = 0
        self.myFunctions = {}
        self.currFunction = None
        self.crossingFunction = False
        self.currDelete = None
        self.falling = False
        #we only have a certain number of functions
        self.functionsStock = [4]*5
        self.posX = None
        self.posY = None
        self.feetX = None
        self.feetY = None
        self.name = "player1"
        #states
        self.dead = False
        self.won = False
    def reset(self):
        self.stars = 0
        self.score = 0
        self.spikes = 0
        self.TNTs = 0
        self.myFunctions = {}
        self.falling = False
        self.dead = False
        self.won = False
        self.crossingFunction = False
