from cmu_112_graphics import *
import os
import time
import random
import bisect
import numpy as np
import math
import requests

#my classes
from functions import Function, polynomial
from terrain import Terrain
from character import Player
#from beautifulsoup4 import BeautifulSoup 
# other important functions
#Source: https://www.cs.cmu.edu/~112/notes/
#notes-data-and-operations.html#FloatingPointApprox

#Modal App Structure: https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
#Midpoint Displacement Reference: https://www.sfu.ca/~rpyke/335/projects/tsai/report1.htm
#Stickman figures: https://github.com/kidscancode (Only images sourced)


def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

def colorCode(r,b,g):
        colorval = "#%02x%02x%02x" % (r, g, b)
        return colorval

def solveQuad(a,b,c):
    discriminant = ((b**2 - 4*a*c)**0.5)
    x1 = (-b + discriminant)/(2*a)
    x2 = (-b - discriminant)/(2*a)
    return random.choice([x1, x2])

def addFunctionDescription(query):
    description = ""
    q = query.replace('', '%20')
    URL = 'www.dictionary.com' + q
    
    page = requests.get(URL)
    results = str(results)
    startIndex = (str(results)).find("[{")
    endIndex = (str(results)).find('}</script>')
    results = results[startIndex:endIndex]

    results = results.split("},")
    return results
           
class MyApp(ModalApp):
    width = 800
    height = 800
    def appStarted(self):
       
        #add a select coordinates marker
        self.selectC1 = (-1,-1)
        self.selectC2 = (-1,-1)

        #setting the modes
        self.SplashScreenMode = SplashScreenMode()
        self.HomeScreenMode = HomeScreenMode()
        self.HelpScreenMode = HelpScreenMode()
        self.StatsScreenMode = StatsScreenMode()
        self.LevelsScreenMode = LevelsScreenMode()
        self.GameMode1 = GameMode1()
        self.wonGameScreen = wonGameScreen()
        self.lostGameScreen = lostGameScreen()
         #important variables
        ModesList = [self.SplashScreenMode, self.HomeScreenMode, self.HelpScreenMode,self.StatsScreenMode, self.LevelsScreenMode, self.GameMode1]
        myPlayer = Player()
        
        for mode in ModesList:
            mode.player = myPlayer
            mode.buttonDim = [[120, 60]]
            
        self.setActiveMode(self.SplashScreenMode)

    def setImages(mode):
        path = 'skyBack.png'
        mode.image1 = mode.loadImage(path)
        mode.image1 = mode.image1.resize((self.width, self.height))
        path = 'Logo.png'
        mode.image2 = mode.loadImage(path)
        mode.image2 = mode.image2.resize((self.width//2, self.height//4))
        path = 'homeMenu/'
        ind = 0
        mode.imagesHome = []
        for file in sorted(os.listdir(path)):
            img = mode.loadImage("homeMenu/" + file)
            img = img.resize((mode.width//3,mode.width//3))
            mode.imagesHome.append(img)
        iconPath = 'gameBar/'
        mode.imagesBar = []
        for file in sorted(os.listdir(iconPath)):
            img = mode.loadImage(iconPath + file)
            img = img.resize((60, 60))
            mode.imagesBar.append(img)
    
    #############################################################################
    #Src: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
    ############################################################################
    @staticmethod
    def getCell(x, y, numRows, numCols, margin):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not MyApp.pointInGrid(x, y,margin)):
            return (-1, -1)
        gridWidth  = MyApp.width - 2*margin
        gridHeight = MyApp.height - 2*margin
        cellWidth  = gridWidth / numRows
        cellHeight = gridHeight / numCols
        row = int((y - margin) / cellHeight)
        col = int((x - margin) / cellWidth)
        return (row, col)
    @staticmethod
    def getCellBounds(row, col, numRows, numCols,margin):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = MyApp.width - 2*margin
        gridHeight = MyApp.height - 2*margin
        cellWidth = gridWidth / numRows
        cellHeight = gridHeight / numCols
        x0 = margin + col * cellWidth
        x1 = margin + (col+1) * cellWidth
        y0 = margin + row * cellHeight
        y1 = margin + (row+1) * cellHeight
        return (x0, y0, x1, y1)
    @staticmethod
    def pointInGrid(x, y,margin):
        # return True if (x, y) is inside the grid defined by app.
        return ((margin <= x <= MyApp.width-margin) and
                (margin <= y <= MyApp.height-margin))

def createButton(canvas, cx, cy, height,width, text, font, txtC, buttonC):
        canvas.create_rectangle(cx-(width/2), cy-(height/2), cx+(width/2), cy+(height/2), fill=buttonC)
        canvas.create_text(cx, cy, text= text, fill=txtC, font = font)

def checkButtonPressed(cx, cy, event, height, width):
        if ((cx - (width/2) <= event.x <= cx+(width/2))
            and (cy-(height/2) <= event.y <= cy+(height/2))):
            return True
        return False
        
class SplashScreenMode(Mode):
    def appStarted(mode):
        mode.setImages()
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,
                            image=ImageTk.PhotoImage(mode.image1))
        canvas.create_text(mode.width/2, 400, text = "Learn more about functions by finding your way through a mysterious path", font="Arial 20 bold")
        createButton(canvas, 400, 600, mode.buttonDim[0][1], mode.buttonDim[0][0], "Play Now!", 'Arial 15 bold', 'white', 'pink')
        canvas.create_image(mode.width/2, mode.height/3, image=ImageTk.PhotoImage(mode.image2))

    def keyPressed(mode, event):
        if (event.key == "Enter"):
            name = mode.getUserInput('What is your name?')
            if (name != None):
                mode.player.name = name
            else:
                mode.player.name = "player1"
            mode.app.setActiveMode(mode.app.HomeScreenMode)
    
    def mousePressed(mode, event):
        val = checkButtonPressed(400, 600, event, mode.buttonDim[0][1], mode.buttonDim[0][0])
        if val:
            name = mode.getUserInput('What is your name?')
            if (name != None):
                mode.player.name = name
            else:
                mode.player.name = "player1"
            mode.app.setActiveMode(mode.app.HomeScreenMode)
    def setImages(mode):
        path = 'skyBack.png'
        mode.image1 = mode.loadImage(path)
        mode.image1 = mode.image1.resize((mode.width, mode.height))
        path = 'Logo.png'
        mode.image2 = mode.loadImage(path)
        mode.image2 = mode.image2.resize((mode.width//2, mode.height//4))

class HomeScreenMode(Mode):
    def appStarted(mode):
        mode.setImages()
        mode.positions = [((mode.width/3 - mode.width/6),(mode.height/2 + mode.height/4)),
                     ((mode.width/3 + mode.width/6), (mode.height/2 - mode.height/4)),
                     ((2*mode.width/3 + mode.width/6), (mode.height/2 + mode.height/4))]
    def setImages(mode):
        path = 'homeMenu/'
        ind = 0
        mode.imagesHome = []
        for file in sorted(os.listdir(path)):
            img = mode.loadImage("homeMenu/" + file)
            img = img.resize((mode.width//3,mode.width//3))
            mode.imagesHome.append(img)


    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height)
        ind = 0
        for (cx,cy) in mode.positions:
            canvas.create_image(cx, cy,
                            image=ImageTk.PhotoImage(mode.imagesHome[ind]))
            ind += 1
        canvas.create_text(mode.positions[0][0], mode.width-50, text="Help", font= "Arial 15 bold")
        canvas.create_text(mode.positions[2][0], mode.width-50, text="My Performance", font= "Arial 15 bold")
        
    def mousePressed(mode, event):
        mode.checkHomeMenuClicked(event)

    def checkHomeMenuClicked(mode,event):
        s = mode.width/3
        ind = 0
        for (cx, cy) in mode.positions:
            if (cx-s//2) <= event.x <= (cx+s//2) and (cy - s//2) <= event.y <= (cy + s//2):
                if ind == 0:
                    mode.app.setActiveMode(mode.app.HelpScreenMode)
                elif ind == 2:
                    mode.app.setActiveMode(mode.app.StatsScreenMode)
                else:
                    mode.app.setActiveMode(mode.app.LevelsScreenMode)
            ind += 1
class HelpScreenMode(Mode):
    def appStarted(mode):
        mode.setImages()
    
    def redrawAll(mode,canvas):
        canvas.create_text(mode.width/2, 25, text="Help and Instructions", font="Helvetica 25 bold")
        canvas.create_image(mode.width/2, mode.height/2, image = ImageTk.PhotoImage(mode.help))
        
    def setImages(mode):
        path = 'Help.png'
        mode.help = mode.loadImage(path)
        mode.help = mode.help.resize((600,600))
        
    def keyPressed(mode, event):
        if (event.key == "Left"):
            mode.app.setActiveMode(mode.app.HomeScreenMode)

class StatsScreenMode(Mode):
    def redrawAll(mode, canvas):
        mode.drawStatsScreen(canvas)
        
    def appStarted(mode):
        mode.setImages()
    def setImages(mode):
        path = "stats/"
        mode.statsImgs = []
        for file in sorted(os.listdir(path)):
            img = mode.loadImage(file)
            img = img.resize((50, 50))
            mode.statsImgs.append(img)
    

    def keyPressed(mode, event):
        if (event.key == "Left"):
            mode.app.setActiveMode(mode.app.HomeScreenMode)

    def playerStats(mode):
        #path to player stats
        try:
            playerStatsP = "stats.csv"
            with open(playerStatsP, 'r') as file:
                reader = csv.reader(file)
                existingFile = []
                for row in reader:
                    existingFile.append(row)
            stats = [0]*4
            for row in existingFile:
                stats[0] += row[1]
                stats[1] += row[2]
                stats[2] += row[3]
                stats[3] += row[3]
            return stats
        except:
            return None
        

    def drawStatsScreen(mode,canvas):
        playerS = mode.playerStats()
        if  playerS == None or len(playerS) == 0:
            canvas.create_text(mode.width/2, mode.height/2, text="Play your first level now!")
        else:
            canvas.create_text(mode.width/2, 50, text="Your Performance")
            canvas.create_image(mode.width/2, 75, img = ImageTk.PhotoImage(mode.statsImg[0]))
            canvas.create_text(mode.width/2, mode.height/5 - 30, text=f"Total Points Earned: {stats[0]}")
            canvas.create_image(mode.width/2, mode.height/5 + 50, img = ImageTk.PhotoImage(mode.statsImg[1]))
            canvas.create_text(mode.width/2, 2*mode.height/5 - 30, text=f"Stars: {stats[1]}")
            canvas.create_image(mode.width/2, 2*mode.height/5 + 50, img = ImageTk.PhotoImage(mode.statsImg[2]))
            canvas.create_text(mode.width/2, 3*mode.height/5 - 30, text=f"Spikes: {stats[2]}")
            canvas.create_image(mode.width/2, 3*mode.height/5 + 50, img = ImageTk.PhotoImage(mode.statsImg[3]))
            canvas.create_text(mode.width/2, 4*mode.height/5 - 30, text= f"Functions Used: {stats[3]}")

class LevelsScreenMode(Mode):
    def appStarted(mode):
        mode.setImages()

    def setImages(mode):
        iconPath = 'gameBar/'
        mode.imagesBar = []
        for file in sorted(os.listdir(iconPath)):
            img = mode.loadImage(iconPath + file)
            img = img.resize((60, 60))
            mode.imagesBar.append(img)
    def redrawAll(mode,canvas):
        mode.levelMenu(canvas)
            
    def levelMenu(mode, canvas):
        tempImage = mode.imagesBar[0]
        tempImage = tempImage.resize((25,25))
        canvas.create_image(25,25,image=ImageTk.PhotoImage(tempImage))
        index = 0
        margin = 50
        for row in range(3):
            for col in range(3):
                if index + 1 in mode.player.levelsCompleted:
                    (x0, y0, x1, y1) = mode.getCellBounds(row, col,3,3,margin)
                    canvas.create_rectangle(x0, y0, x1, y1,outline='black')
                    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f"{index + 1}", font = "Helvetica 20 bold", fill='black')
                    index += 1

        positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        #add the next level
        if (len(mode.player.levelsCompleted) == 0):
            nextLevel = 1
            (x0, y0, x1, y1) = MyApp.getCellBounds(positions[nextLevel-1][0], positions[nextLevel-1][1],3,3,margin)
            canvas.create_rectangle(x0, y0, x1, y1,outline='black')
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f"{nextLevel}",fill='black')
        elif mode.player.levelsCompleted[-1] + 1 < 10:
            nextLevel = self.player.levelsCompleted[-1] + 1
            (x0, y0, x1, y1) = MyApp.getCellBounds(positions[nextLevel-1][0], positions[nextLevel-1][1],3,3,margin)
            canvas.create_rectangle(x0, y0, x1, y1,outline='black')
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f"{nextLevel}",fill='black')

    def mousePressed(mode, event):
        mode.checkIfLevelPressed(event)
    def checkIfLevelPressed(mode,event):
        if 0 <= event.x <= 50 and 0 <= event.y <= 50:
            mode.app.setActiveMode(mode.app.HomeScreenMode)
        else:
            positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
            (row,col) = MyApp.getCell(event.x,event.y,3,3,50)
            if (row,col) != (-1,-1):
                for (rowL,colL) in positions:
                    if (rowL,colL) == (row,col):
                        ind = positions.index((rowL,colL))
                        mode.player.currLevel = ind + 1
                        mode.app.setActiveMode(mode.app.GameMode1)

class GameMode1(Mode):
    def appStarted(mode):
        mode.setImages()
        mode.selectionMode = False
        mode.init = True
        mode.select1 = (-1,-1)
        mode.select2 = (-1,-1)
        mode.terrain = Terrain(600,600,2,mode.player.currLevel)
        mode.colorChoice = random.randint(0,6)
        mode.last_time = time.time()
        mode.myAng = 90
        #each level will have 3 frames
        mode.frame = 0
        mode.startInd = 0
        mode.endInd = 0
        mode.getStartEndInd(mode.terrain.terrainFills[mode.player.currLevel-1])
        mode.currPt = 0
        mode.addFrame = [False, False]
        mode.deleteFrame = False
        mode.editFrame = [False, False]
        mode.entered = False
        mode.spikesCounts = mode.terrain.spikesLocs[mode.player.currLevel-1]
        mode.runFunction = False
        mode.player.crossingFunction = False
        mode.error = False

        #mode.player.reset()

    def setImages(mode):
        iconPath = 'gameBar/'
        mode.imagesBar = []
        for file in sorted(os.listdir(iconPath)):
            img = mode.loadImage(iconPath + file)
            img = img.resize((60, 60))
            mode.imagesBar.append(img)
        mode.player_frames = []
        for path in mode.player.frames_r:
            img = mode.loadImage(path)
            img = img.resize((40,40))
            mode.player_frames.append(img)
        (mode.playerWidth, mode.playerHeight) = mode.player_frames[0].size
        #for functions panel
        path = 'backButton.png'
        mode.backButton = mode.loadImage(path)
        mode.backButton = mode.backButton.resize((25,25))

    def redrawAll(mode, canvas):
        if mode.error == True:
            mode.drawMessage(canvas, "Error in creating function")
        mode.drawLevel(canvas, mode.terrain.terrainFills[mode.player.currLevel-1], mode.terrain.breaksTot[mode.player.currLevel-1], (100,100), (700, 700), mode.colorChoice)
        mode.addGameBar(canvas)
        mode.drawStars(canvas, 15)
        mode.drawFunctions(canvas)
        if mode.player.dead == True:
            mode.lostGame()
        elif mode.player.won == True:
            mode.wonGame()
        if mode.selectionMode:
            mode.drawMessage(canvas, "Please press 's' to clear/exit selection mode")
            mode.drawHighlighterTool(canvas)
        if mode.addFrame[0] == True:
            mode.functionMenu(canvas)
        elif mode.addFrame[1] == True:
            mode.parameterEntry(canvas)
        
            
    def drawMessage(mode, canvas, message):
        canvas.create_text(mode.width-350,50,text=message, font="Arial 10")
    def mousePressed(mode, event):
        mode.checkIfGameBarPressed(event)
        if mode.selectionMode:
            mode.updateSelection(event)
        if mode.addFrame[0] == True:
            val = mode.checkIfMenu1Pressed(event)
            if val:
                mode.addFrame[0] = False
                mode.addFrame[1] = True
            val = mode.checkIfBackPressed(event)
            if val:
                mode.addFrame[0] = False
                mode.addFrame[1] = False
        elif mode.addFrame[1] == True:
            val = mode.checkIfAddButtonPressed(event)
            mode.checkIfMenu2Pressed(event)
            val2 = mode.checkIfBackPressed(event)
            if val:
                ind = Function.functions.index(mode.player.currFunction[1])
                mode.player.functionsStock[ind] -= 1
                mode.addFunctionToModel()
                mode.addFrame[0] = False
                mode.addFrame[1] = False
            if val2:
                mode.addFrame[0] = False
                mode.addFrame[1] = False
        

    def updateSelection(mode, event):
        if 100 <= event.y <= 700 and 100 <= event.x <= 700: 
            if mode.select1 != (-1,-1) and mode.select2 != (-1,-1):
                    mode.select1 = (-1,-1)
                    mode.select2 = (-1,-1)
            if mode.select1 == (-1,-1):
                mode.select1 = (event.x, event.y)
            elif mode.select2 == (-1,-1):
                mode.select2 = (event.x, event.y)
                if mode.select1[0] <= mode.player.posX <= mode.select2[0] or mode.select2[0] <= mode.player.posX <= mode.select1[0]:
                    mode.select1 = (-1,-1)
                    mode.select2 = (-1,-1)
                    
    def checkIfBackPressed(mode, event):
        if 12.5 <= event.x <= 37.5 and (700-12.5) <= event.y <= (700+12.5):
            return True
        return False

    def drawDeleteMenu(mode,canvas,colors):
        canvas.create_image(25, 700, image=ImageTk.PhotoImage(mode.backButton))
        totNumFunctions = len(mode.player.myFunctions)
        if totNumFunctions == 0:
            canvas.create_text(mode.width//2, 750, text="No functions added yet", font="Arial 15 bold")
            return
        cols = totNumFunctions//3
        
        count = 0
        for row in range(3):
            for col in range(cols+1):
                if count < len(mode.player.myFunctions):
                    if colors[count] != None:
                        canvas.create_rectangle((100 + col*100)-50, (725 + 25*row)-12.5, (100 + col*100)+50, (725 + 25*row)+12.5,
                                                fill = 'yellow', width=0)
                canvas.create_text(100 + col*100, 725 + 25*row, text = f"{mode.player.myFunctions[key[count]]}", font = "Arial 10 bold")
                count += 1
        createButton(canvas,650, 750, mode.buttonDims[0][1]//2, mode.buttonDims[0][0], "Delete", "Arial 10", 'white', 'pink')
    def isDeleteMenuPressed(mode,event):
        totNumFunctions = len(mode.player.myFunctions)
        if totNumFunctions > 0:
            cols = totNumFunctions//3
            count = 0
            removeFunctions  = []
            for row in range(3):
                for col in range(cols+1):
                    if count < len(mode.player.myFunctions):
                        if (100 + col*100)-50 <= event.x <= (100 + col*100)+50 and (725 + 25*row)-12.5 <= event.y <= (725 + 25*row)+12.5:
                            mode.removeFunction.append(mode.keys[count])
                            mode.colors[count] = 'select'
                        count += 1

    def checkDeleteButtonPressed(mode,event):
        val = checkButtonPressed(650, 750, event, mode.buttonDims[0][1]//2, mode.buttonDims[0][0])
        for key in mode.removeFunction:
            mode.player.myFunctions.pop(key)
        mode.deleteFrame = False
        mode.refreshDeleteVars()

    def refreshDeleteVars(mode):
        mode.colors = [None]*len(mode.player.myFunctions)
        mode.keys = []
        for key in mode.player.myFunctions:
            mode.keys.append(key) 
        
        
    def keyPressed(mode, event):
        if event.key == "s":
            mode.selectionMode = not mode.selectionMode
            if mode.selectionMode == False:
                mode.select1 = mode.select2 = (-1,-1)
        if event.key == "r":
            mode.init = True
        if event.key == "Right" and mode.player.falling == False:
            mode.animate()
            mode.collideWithStar(15)
            mode.collideWithSpike()
            mode.checkFallInGaps(mode.terrain.breaksTot[mode.player.currLevel-1])
        if event.key == "Right" and mode.player.falling == True:
            mode.falling()
        if event.key == "p":
            mode.player.currLevel = 4
            mode.init = True
        if event.key == "Down":
            mode.moveFunction()
    def timerFired(mode):
        if mode.player.falling:
            mode.falling()
        if mode.runFunction:
            mode.moveFunction()
    def drawHighlighterTool(mode,canvas):
        if mode.select1 != (-1,-1): 
            canvas.create_line(mode.select1[0], 700,
                               mode.select1[0],100, fill='blue')
        if mode.select2 != (-1,-1):
            canvas.create_line(mode.select2[0], 700,
                               mode.select2[0],100, fill='blue')
            
    def drawLevel(mode, canvas, terrainFill, breakPts, startPixel, endPixel, colorChoice):
        canvas.create_rectangle(startPixel[0], startPixel[1], endPixel[0], endPixel[1], fill = colorCode(117, 218, 255))
        colorsDict = {'0': (195, 157, 224), '1': (158, 98, 204),
                          '2': (130, 79, 138), '3': (68, 28, 99), '4': (49, 7, 82),
                          '5': (23, 3, 38), '6': (240, 203, 163)}
        
        colorTup = colorsDict[str(colorChoice)]
        layer = []
        for i in range(mode.startInd, mode.endInd-1):
            if i+1 < len(terrainFill):
                transformedValX2 = terrainFill[i][0] - (mode.frame*600)
                transformedValY2 = terrainFill[i][1]
                transformedValX1 = terrainFill[i+1][0] - (mode.frame*600)
                transformedValY1 = terrainFill[i+1][1]
                if (100 <= transformedValX2 <= 700 or 100 <= transformedValX1 <= 700)  and breakPts[i] == False:
                    layer += [(transformedValX2,transformedValY2)]
                    if terrainFill[i+1][0]-terrainFill[i][0] > 1:
                        m = float(transformedValY1-transformedValY2)/(transformedValX1-transformedValX2)
                        n = transformedValY2-m*transformedValX2
                        r = lambda x: m*x+n  # straight line formula
                        valsArr = np.arange(transformedValX2+1, transformedValX1, 1)
                        for val in valsArr:
                            if 100 <= val <= 700:
                                layer += [(val, r(val))]
                        if mode.spikesCounts.count(i) != 0:
                            if mode.init == True:
                                print(i)
                            mode.drawSpikes(canvas, transformedValX2, transformedValY2,transformedValX1, transformedValY1)

        for (x, y) in layer:
            canvas.create_line(x, y, x, 700, fill=colorCode(colorTup[0], colorTup[1], colorTup[2]), width = 1)
        mode.completeLayer = layer  
        mode.drawEntrance(canvas)
        mode.drawTarget(canvas)
        mode.entered = True
        if mode.init != True:
            #place character
            canvas.create_image(mode.player.posX, mode.player.posY, image=ImageTk.PhotoImage(mode.player_frames[mode.player.currFrame]))
            #place functions: TBD
        else:
            mode.levelRestart()

    def levelRestart(mode):
        mode.pickEntrance()
        mode.select1 = (-1,-1)
        mode.select2 = (-1,-1)
        #mode.player.reset()
        mode.init = False
        

    def falling(mode):
        mode.player.posY += 5
        if 600 <= mode.player.posY <= 700:
            mode.player.dead = True
        
    def animate(mode):
        mode.setImages()
        if mode.player.posX < 100 and mode.frame == 0:
            mode.player.posX += 10
            now = time.time()
            if now - mode.last_time > 0.05:
                mode.last_time = now
                mode.player.currFrame = (mode.player.currFrame + 1) % 4
        elif mode.player.posX >= 700 - mode.playerWidth/2 and mode.frame == 2:
            mode.player.posX += 10
            now = time.time()
            if now - mode.last_time > 0.05:
                mode.last_time = now
                mode.player.currFrame = (mode.player.currFrame + 1) % 4
        elif mode.player.crossingFunction:
            mode.player.posX += 10
            functionCollided = mode.getCollidingFunction()
            mode.player.posY -= dx*functionCollided.getDerivative(mode.player.posX-1)
            mode.functionCollided.getDerivative(mode.player.posX-1)
            mode.myGrad = functionCollided.getDerivative(mode.player.posX-1)
            mode.myAng = math.degrees(math.atan(mode.myGrad))
            #rotate image
            if mode.myGrad > 0:
                mode.player_frames[mode.player.currFrame] = mode.player_frames[mode.player.currFrame].rotate(mode.myAng)
            if mode.myGrad < 0:
                mode.player_frames[mode.player.currFrame] = mode.player_frames[mode.player.currFrame].rotate(360 - (180-mode.myAng))

            if now - mode.last_time > 0.05:
                mode.last_time = now
                mode.player.currFrame = (mode.player.currFrame + 1) % 4
        else:
            clusterSize = 3
            mode.myAng, mode.myGrad = mode.findGradient(mode.currPt, clusterSize)
            if mode.myGrad > 0:
                mode.player_frames[mode.player.currFrame] = mode.player_frames[mode.player.currFrame].rotate(mode.myAng)
            if mode.myGrad < 0:
                mode.player_frames[mode.player.currFrame] = mode.player_frames[mode.player.currFrame].rotate(360 - (180-mode.myAng))
            
            dx = mode.movePt()
            mode.player.posX += dx
            mode.player.posY += dx*mode.myGrad
            now = time.time()
            if now - mode.last_time > 0.05:
                mode.last_time = now
                mode.player.currFrame = (mode.player.currFrame + 1) % 4
            if mode.player.posX >= 700 - mode.playerWidth/2: 
                mode.frame += 1
                mode.player.posX = 100
                #update the start and end indices
                mode.getStartEndInd(mode.terrain.terrainFills[mode.player.currLevel-1])
                sizePerFrame = len(mode.terrain.terrainFills[mode.player.currLevel-1])//3
                mode.player.posY = mode.terrain.terrainFills[mode.player.currLevel-1][mode.startInd][1]
    
    def movePt(mode):
        layer = mode.terrain.terrainFills[mode.player.currLevel-1]
        ind = mode.currPt
        i = 1
        while True:
            if ind + i < len(layer):
                if layer[ind+i][0] > layer[ind][0] + 5:
                    mode.currPt = ind + i
                    return layer[ind+i][0] - layer[ind][0]
            i += 1
        return 5
        

    def getStartEndInd(mode, terrainFill):
        mode.startInd = mode.endInd
        for i in range(len(terrainFill)):
            if terrainFill[i][0] <= 100 + (mode.frame+1)*600:
                mode.endInd = i
            else:
                break

    def findGradient(mode, currPoint, clusterSize):
        ind = currPoint
        terrain = tuple(mode.terrain.terrainFills[mode.player.currLevel-1])
        if ind + clusterSize + 1 <= len(terrain):
            if terrain[ind][0] - terrain[ind+clusterSize][0] != 0:
                gradient = (terrain[ind][1] - terrain[ind+clusterSize][1])/(terrain[ind][0] - terrain[ind+clusterSize][0])
            else:
                gradient = 0
        else:
            gradient = (terrain[ind][1] - terrain[ind-clusterSize][1])/(terrain[ind][0] - terrain[ind-clusterSize][0])
        return (math.degrees(math.atan(gradient)), gradient)
    
    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x0 - x1)**2 + (y1 - y1)**2)**0.5
    def pickEntrance(mode):
        originalH =  mode.terrain.terrainFills[mode.player.currLevel-1][0][1]
        mode.player.posX = 50
        mode.player.posY = originalH - mode.playerWidth/2
    def drawEntrance(mode,canvas):
        originalH =  mode.terrain.terrainFills[mode.player.currLevel-1][0][1]
        canvas.create_line(0, originalH, 100, originalH, width = 7, fill="black")

    def drawTarget(mode, canvas):
        finalH = mode.terrain.terrainFills[mode.player.currLevel-1][-1][1]
        canvas.create_rectangle(700, finalH-50, 800, finalH, width = 6, fill="gold")
        canvas.create_text(750, finalH-25, text="TARGET", font="Arial 15 bold")
    
    def addGameBar(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,100,fill='pink',width=6)
        #iconHolder
        margin = 50
        for i in range(len(mode.imagesBar)):
            canvas.create_image(i*60 + margin, 50, image=ImageTk.PhotoImage(mode.imagesBar[i]))
        canvas.create_text(mode.width-100, 25, text=f"{mode.player.name}")
        canvas.create_text(mode.width-50,25, text=f"Score: {mode.player.score}")
        canvas.create_text(mode.width-100,50, text=f"Stars: {mode.player.stars}")
        canvas.create_text(mode.width-50,50, text=f"TNT: {mode.player.TNTs}")

    def drawSpikes(mode, canvas, startX, startY, endX, endY):
        midPointX = (startX + endX)/2
        midPointY = (startY + endY)/2
        midPointY += 10
        canvas.create_polygon(startX, startY, midPointX, midPointY, endX, endY, fill='black')
        
    def drawStars(mode, canvas, r):
        for i in range(len(mode.terrain.starPos[mode.player.currLevel-1])):
            (x, y) = mode.terrain.starPos[mode.player.currLevel-1][i]
            transformedValX = x - (mode.frame*600)
            if 100 <= transformedValX <= 700:
                center_x = transformedValX
                center_y = y - r
                points=[center_x-int(r*math.sin(2*math.pi/5)),
                        center_y-int(r*math.cos(2*math.pi/5)),
                        center_x+int(r*math.sin(2*math.pi/5)),
                        center_y-int(r*math.cos(2*math.pi/5)),
                        center_x-int(r*math.sin(math.pi/5)),
                        center_y+int(r*math.cos(math.pi/5)),
                        center_x,
                        center_y-r,
                        center_x+int(r*math.sin(math.pi/5)),
                        center_y+int(r*math.cos(math.pi/5))]
                canvas.create_polygon(points,outline='green',width=0,fill='yellow')
            
    def checkIfGameBarPressed(mode,event):
        mode.error = False
        if 20 <= event.y <= 80 and 20 <= event.x <= 80:
            mode.app.setActiveMode(mode.app.HomeScreenMode)
        elif mode.width-125 <= event.x <= mode.width and 20 <= event.y <= 80:
            name = mode.getUserInput('What is your name?')
            if (name != None):
                mode.player.name = name
        elif 20 <= event.y <= 80 and 80 <= event.x <= 140:
            mode.addFrame[0] = True
        elif 20 <= event.y <= 80 and 140 <= event.x <= 200:
            mode.editFrame = True
        elif 20 <= event.y <= 80 and 200 <= event.x <= 260:
            mode.deleteFrame[0] = True
        elif 20 <= event.y <= 80 and 260 <= event.x <= 320:
              mode.runFunction = True
              mode.refreshDeleteVars()

    def functionMenu(mode,canvas):
        index = 0
        margin = 50
        canvas.create_image(50, 720, image=ImageTk.PhotoImage(mode.backButton))
        for row in range(1):
            for col in range(6):
                cx = 125 + 100*col
                cy = 750
                l =  50
                canvas.create_rectangle(cx-l, cy-l, cx+l, cy+l,outline='black')
                if mode.player.functionsStock[col] != 0:
                    canvas.create_text(cx, cy, text= Function.functions[col], font= "Arial 10 bold")
    
    def parameterEntry(mode, canvas):
        canvas.create_image(25, 700, image=ImageTk.PhotoImage(mode.backButton))
        #title
        canvas.create_text(50, 725, text= mode.player.currFunction[1],font= "Arial 10 bold")
        #name/key
        mode.player.currFunction[0] = f"function{len(mode.player.myFunctions)}"
        canvas.create_text(50, 740, text= f'function{len(mode.player.myFunctions)}',font= "Arial 10 bold")
        #description
        #description = queryDescription(mode.player.currFunction[0])
        #canvas.create_text(30, self.width/2, text= description,font= "Arial 30")
        mode.player.currFunction[7] = polynomial.degrees[mode.player.currFunction[1]] 
        canvas.create_text(50, 760, text= f"Degree: {mode.player.currFunction[7]}",font= "Arial 10 bold")
        params = polynomial.params[mode.player.currFunction[1]]
        canvas.create_text(125, 750, text=f"{polynomial.getExpression(mode.player.currFunction[1],mode.player.currFunction[7])}", font = "Arial 10 bold")
        count = 0
        for row in range(3):
            for col in range(2):
                if count < len(params):
                    canvas.create_text(250 + 150*col, 725 + 25*row, text=f"Change coefficient {params[count]}")
                count += 1
        canvas.create_text(550, 725, text="Start coordinates.")
        canvas.create_text(550, 775, text="End coordinates.")
        createButton(canvas, 700, 750, mode.buttonDim[0][1]//2, mode.buttonDim[0][0], "Add function" , "Arial 10 bold", 'white', 'pink')
        
    def checkIfMenu2Pressed(mode, event):
        length = 50
        count = 0
        for row in range(3):
            for col in range(2):
                if  (250 + 150*col)-length <= event.x <= (250 + 150*col)+length:
                    if (725 + 25*row)-length <= event.y <= (725 + 25*row)+length:
                        if count < len(polynomial.params[mode.player.currFunction[1]]):
                            param = mode.getUserInput(f"What is the value of {polynomial.params[mode.player.currFunction[1]][count]}?")
                            try:
                                mode.player.currFunction[5][count] = float(param)
                                break
                            except:
                                pass
                                
                count += 1
        if 550 - length <= event.x <= 550 + length and 725 - length <= event.y <= 725 + length:
            while True:
                x = mode.getUserInput(f"What is the value of start x coordinate?")
                try:
                    float(x)
                    break
                except:
                    x = mode.getUserInput(f"What is the value of start x coordinate?")
            mode.player.currFunction[2] = float(x)
        elif 550 - length <= event.x <= 550 + length and 775 - length <= event.y <= 775 + length:
            while True:
                x = mode.getUserInput(f"What is the value of end x coordinate?")
                try:
                    float(x)
                    break 
                except:
                    x = mode.getUserInput(f"What is the value of end x coordinate?")
            mode.player.currFunction[3] = float(x)

    def addFunctionToModel(mode):
        if mode.select1 == (-1, -1) or mode.select2 == (-1,-1):
            mode.error = True
            return
        if mode.select1[0] < mode.select2[0]:
            mode.player.currFunction[4] = [mode.select1, mode.select2]
        else:
            mode.player.currFunction[4] = [mode.select2, mode.select1]
            
        for attr in mode.player.currFunction:
            if attr == None:
                mode.error = True
                return 
        
        mode.player.myFunctions[mode.player.currFunction[0]] = polynomial(mode.player.currFunction[0], mode.player.currFunction[1], mode.player.currFunction[2],
                                                                       mode.player.currFunction[3], mode.player.currFunction[4], mode.player.currFunction[5],
                                                                       mode.player.currFunction[6], mode.player.currFunction[7])
        mode.player.score += 10*(Function.functions.index(mode.player.currFunction[1])+1)
        mode.placeFunction()
        
    def collideWithStar(mode, r):
        star_pos_remove = []
        for i in range(len(mode.terrain.starPos[mode.player.currLevel-1])):
            (x, y) = mode.terrain.starPos[mode.player.currLevel-1][i]
            transformedValX = x - (mode.frame*600)
            if 100 <= transformedValX <= 700:
                center_x = transformedValX
                center_y = y - r
                if y <= mode.player.posY <= center_y + r and center_x - r <= mode.player.posX <= center_x + r:
                    mode.player.stars += 1
                    mode.player.score += 10
                    star_pos_remove.append((x,y))
        for i in range(len(star_pos_remove)):
            mode.terrain.starPos[mode.player.currLevel-1].remove(star_pos_remove[i])

    def collideWithSpike(mode):
        layer = mode.terrain.terrainFills[mode.player.currLevel - 1]
        for i in range(len(mode.spikesCounts)):
            transformedX = mode.player.posX  + (mode.frame*600)
            feetY = mode.player.posY + mode.playerHeight/2
            ind1 = mode.spikesCounts[i]
            ind2 = ind1 + 1
            if layer[ind1][0] < transformedX < layer[ind2][0] and layer[ind1][1] < feetY < layer[ind2][1]:
                    mode.player.spikes += 1
                    if mode.player.score > 10:
                        mode.player.score -= 10
                    mode.player.dead = True
    
    def checkIfMenu1Pressed(mode, event):
        for col in range(6):
            l = 50
            cx = 125 + 100*col
            cy = 750
            if cx - l <= event.x <= cx + l:
                if cy - l <= event.y <= cy + l:
                    if Function.functions[col] == "Square Root":
                        mode.player.currFunction = [None, None, None, None, None, None, [0,0], 0.5]
                    else:
                        degree = polynomial.degrees[Function.functions[col]]
                        mode.player.currFunction = [None, None, None, None, None, [None]*(degree+1), [0,0], degree]
                    mode.player.currFunction[1] = Function.functions[col]
                    return True
        return False
    def checkIfAddButtonPressed(mode, event):
        return checkButtonPressed(650, 750, event, mode.buttonDim[0][1]//2, mode.buttonDim[0][0])

    def checkFallInGaps(mode, breakPts):
        transformedX = mode.player.posX  + (mode.frame*600)
        for i in range(len(breakPts)):
            if breakPts[i] and not mode.player.crossingFunction:
                x1 = mode.terrain.terrainFills[mode.player.currLevel-1][i][0]
                x2 = mode.terrain.terrainFills[mode.player.currLevel-1][i+1][0]
                if x1 <= transformedX <= x2:
                    mode.player.falling = True
                    mode.player.posX += mode.playerWidth/2
                
    def lostGame(mode):
        mode.saveStats()
        mode.app.setActiveMode(mode.app.lostGameScreen)
    def wonGame(mode):
        mode.app.setActiveMode(mode.app.wonGameScreen)
        mode.saveStats()

    def updateFunctionsStock(mode):
        for function in mode.player.myFunctions:
            category = function.category
            ind = Function.functions.index(category)
            mode.player.functionsStock[ind] -= 1

    def saveStats(mode):
        path = "stats.csv"
        fields = [mode.player.currLevel, mode.player.score, mode.player.stars, mode.player.spikes, len(mode.player.myFunctions)]
        with open(path, 'w') as file:
            writer = writer.csv(file)
            writer.writerow(fields)

    def placeFunction(mode):
        #selecting the last function to place
        stF = (mode.player.myFunctions[mode.player.currFunction[0]].startCoords)
        endF = (mode.player.myFunctions[mode.player.currFunction[0]].endCoords)
        transformedStF = stF + (600*mode.frame)
        transformedEndF = endF + (600*mode.frame)
        stP = (mode.player.myFunctions[mode.player.currFunction[0]].showCoords[0][0])
        endP = (mode.player.myFunctions[mode.player.currFunction[0]].showCoords[1][0])
        samples = ((endP - stP)//5)+1
        pixelInterval = np.arange(stP, endP, samples)
        coords = mode.player.myFunctions[mode.player.currFunction[0]].getCoords(samples)
        mode.player.myFunctions[mode.player.currFunction[0]].setPixelInterval(pixelInterval)
        mode.player.myFunctions[mode.player.currFunction[0]].setCartesianCoords(coords)
        mode.player.myFunctions[mode.player.currFunction[0]].setTransformedCoords(coords)
        minY = mode.findMin(coords)
        maxY = mode.findMax(coords)
        diff = 100-maxY
        mode.player.myFunctions[mode.player.currFunction[0]].applyTransformation([0,maxY+diff])
      
            
    def findMin(mode,coords):
        y = []
        for i in range(len(coords)):
            y.append(coords[i][1])
        return min(y)
    def findMax(mode,coords):
        y = []
        for i in range(len(coords)):
            y.append(coords[i][1])
        return max(y)
    def drawFunctions(mode, canvas):
        for key in mode.player.myFunctions:
            function = mode.player.myFunctions[key]
            pixelInterval = function.pixelInterval
            finalCoords = function.finalCoords
            for i in range(len(pixelInterval)):
                transformedX = pixelInterval[i] - (600*mode.frame)
                if 100 <= finalCoords[i][1] <= 700: 
                    canvas.create_oval(pixelInterval[i] - 5, finalCoords[i][1] - 5, pixelInterval[i] + 5, finalCoords[i][1] + 5, fill='blue')

    def moveFunction(mode):
        for key in mode.player.myFunctions:
            function = mode.player.myFunctions[key]
            if function.move == True:
                function.applyTransformation([0,5])
                #mode.functionCollidesWithTerrain(key)
        
    def functionCollidesWithTerrain(mode, key):
        layer = mode.completeLayers
        function = mode.player.myFunctions[mode.player.currFunction[0]]
        for i in range(len(function.finalCoords)):
            for j in range(len(layer)):
                if (GameMode1.distance(function.pixelInterval[i][0], layer[j][0], function.finalCoords[i][1], layer[j][1]) <= 5):
                    mode.player.myFunctions[key].move = False
                
    
class lostGameScreen(Mode):
    def appStarted(mode):
        mode.setImages()

    def setImages(mode):
        path = 'lost.png'
        mode.lost = mode.loadImage(path)
        mode.lost = mode.lost.resize((100,100))

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill='black')
        canvas.create_text(mode.width/2, 300, text="Oh no! You lost", font = "Arial 40 bold",fill='white')
        info = [mode.player.score, mode.player.stars, mode.player.spikes, len(mode.player.myFunctions)]
        infoTxt = ["Score", "Stars", "Spikes", "Functions Used"]
        for i in range(len(info)):
            canvas.create_text(mode.width, 400 + 25*i, text=f"{infoTxt[i]}: {info[i]}", fill='white', font="Arial 20")
        create_button(canvas, mode.width, 550, buttonsDim[0][1], mode.buttonsDim[0][0], "Restart", "Arial 15 bold", 'white', 'pink')
    def mousePressed(mode, event):
        val = checkIfButtonPressed(mode.width/2, 550, event, mode.buttonDim[0][1], mode.buttonDim[0][0])
        if val:
            mode.app.setActiveMode(mode.app.GameMode1)
            mode.deleteEntry()
    def deleteEntry(mode):
        f = open("stats.csv", "r+w")
        lines=f.readlines()
        lines=lines[:-1]

        cWriter = csv.writer(f, delimiter=',')
        for line in lines:
            cWriter.writerow(line)

class wonGameScreen(Mode):
    def appStarted(mode):
        mode.setImages()
        

    def setImages(mode):
        path = 'trophy.png'
        mode.won = mode.loadImage(path)
        mode.won = mode.won.resize((100,100))

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height,fill='black')
        canvas.create_image(mode.width/2, 150, image=ImageTk.PhotoImage(mode.won))
        canvas.create_text(mode.width/2, 300, text="Yay! You passed this level", font = "Arial 40 bold",fill='white')
        info = [mode.player.score, mode.player.stars, mode.player.spikes, len(mode.player.myFunctions)]
        infoTxt = ["Score", "Stars", "Spikes", "Functions Used"]
        for i in range(len(info)):
            canvas.create_text(mode.width, 400 + 25*i, text=f"{infoTxt[i]}: {info[i]}", fill='white', font="Arial 20")
        if mode.player.currLevel < 5:
            create_button(canvas, mode.width, 550, buttonsDim[0][1], mode.buttonsDim[0][0], "Next Level", "Arial 15 bold", 'white', 'pink')
        else:
            create_button(canvas, mode.width, 550, buttonsDim[0][1], mode.buttonsDim[0][0], "Your done!", "Arial 15 bold", 'white', 'pink')
            
            
    def mousePressed(mode, event):
        val = checkIfButtonPressed(mode.width/2, 550, event, mode.buttonDim[0][1], mode.buttonDim[0][0])
        if val:
            if mode.player.currLevel < 5:
                mode.player.currLevel += 1 
                mode.app.setActiveMode(mode.app.GameMode1)
            else:
                mode.app.setActiveMode(mode.app.HomeScreenMode)
                
    def checkIfBackPressed(mode, event):
        return checkIfButtonPressed(50, 620, event, mode.buttonDim[0][1], mode.buttonDim[0][0])        


def getCollidingFunction(mode):
    for function in mode.player.myFunctions:
        function = mode.player.myFunctions[key]
        feetY = mode.player.posY - mode.playerHeight/2
        pixelInterval = function.pixelInterval
        finalCoords = function.finalCoords
        for i in range(len(finalCoords)):
            if finalCoords[i][1] - 5 <= feetY <= finalCoords[i][1] + 5 and pixelInterval[i] - 5 <= mode.player.posX <= pixelInterval[i] + 5:
                    mode.player.crossingFunction = True
                    return function
            else:
                mode.player.crossingFunction = False
                return None
                
    
def reflect(mode, key):
    reflectCoords = None
    if key == "h":
        cartesianCoords = mode.player.myFunctions[mode.player.currFunction[0]].cartesianCoords
        reflectCoords = Function.reflectH(coords)
    elif key == "v":
        cartesianCoords = mode.player.myFunctions[mode.player.currFunction[0]].cartesianCoords
        reflectCoords = Function.reflectV(coords)
    if reflectCoords != None:
        mode.player.myFunctions[mode.player.currFunction[0]].setTransformedCoords(reflectCoords)
        minY = mode.findMin(reflectCoords)
        maxY = mode.findMax(reflectCoords)
        diff = 100-maxY
        mode.player.myFunctions[mode.player.currFunction[0]].applyTransformation([0,maxY+diff])

def rotate(mode):
    angle = 20
    cartesianCoords = mode.player.myFunctions[mode.player.currFunction[0]].cartesianCoords
    pixelInterval = mode.player.myFunctions[mode.player.currFunction[0]].pixelInterval
    for i in range(len(cartesianCoords)):
        dist = GameMode1.distance(pixelInterval[i], cartesianCoords[i][1], 0, 0)
        pixelInterval[i] *= math.cos(angle)
        cartesianCoords[i][1] *= math.sin(angle) 
    mode.player.myFunctions[mode.player.currFunction[0]].setTransformedCoords(cartesianCoords)
    minY = mode.findMin(cartesianCoords)
    maxY = mode.findMax(cartesianCoords)
    diff = 100-maxY
    mode.player.myFunctions[mode.player.currFunction[0]].applyTransformation([0,maxY+diff])
#TODO today - delete function, spike stars, function crossing, lost game + won game
#Possible imrpovements (tom) - messagebox addition + energy bar + reflect 
    
def main():
    MyApp(width=800,height=800)

if __name__ == '__main__':
    main()

