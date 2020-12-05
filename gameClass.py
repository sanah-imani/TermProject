from cmu_112_graphics import *
import os
import time
import random
import bisect
import numpy as np
import math
import requests
#from beautifulsoup4 import BeautifulSoup 
# other important functions
#Source: https://www.cs.cmu.edu/~112/notes/
#notes-data-and-operations.html#FloatingPointApprox
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

class Function(object):
    functions = ['Sine', 'Cosine','Circle', 'Ellipse', 'Polynomials','Piecewise']
    myFunctions = {}
    params = {'Sine': ['A','B', 'C'],
              'Cosine': ['A','B', 'C'],
              'Circle': ['a','b','r'],
              'Ellipse': ['a','b'],
              'Polynomials': ['degree'],
              #might remove this 
              'Piecewise': []
              }
    def __init__(self, key, category, startCoords, endCoords, showCoords):
        self.startCoords = startCoords
        self.endCoords = endCoords
        self.showCoords = showCoords
        self.key = key
        self.category = category
        self.move = True
    def getFunctions(self):
        return self.functions
    #change position???
    def placeFunction(function, terrain):
        allCoordsX = function.getCoords()
        for (funcX, funcY) in allCoords:
            for (pointX,pointY) in terrain.groundCoords:
                if almostEqual(funcX, pointX) and almostEqual(funcY, pointY):
                    self.move = False
    def isMoving(self):
        return self.move
    def getTransformations(self):
        return self.transformation
    def updateFunction(self, transformation):
        #here transformation is a four-length list
        #consisting of vertical, horizontal compressions/stretches
        #and horizontal and vertical movement
        self.transformation = transformation
    def addFunction(name,function):
        if isinstance(function, Function):
            Function.myFunctions[name] = function
    def removeFunction(name, function):
        if name in myFunctions:
            Function.myFunctions.pop(name,None)

#polynomial
class polynomial(Function):
    def __init__(self, key, category, startCoords, endCoords, showCoords, coeffs, transformation, degree):
        super().__init__(key, category, startCoords, endCoords, showCoords)
        self.degree = degree
        self.coeffs = coeffs
        self.transformation = transformation
    def __repr__(self):
        finalString = ""
        for i in range(self.degree,-1, -1):
            alphInd = self.degree - i
            coeffAlph = string.ascii_uppercase[alphInd]
            finalString += coeffAlph + f'x^{i}' + "+ "
        #stripping off the laast two characters
        finalString = finalString[:-2]
        return finalString
    def getCoords(self):
        x = np.arrange(showCoords[0], showCoords[1],0.1)
        y = []
        for i in range(len(x)):
            intermed = 0
            for j in range(len(self.coeffs)+1):
                intermed += (self.coeffs[j]*(x[i])**(self.degree-j))
            y += [intermed]
        allCoords = []
        for i in range(len(x)):
            allCoords.append(x[i],y[i])
        return allCoords
    def getDerivative(self,pointX):
        finalAns = 0
        for i in range(len(self.coeffs)+1):
            finalAns += (self.degree-j)*(self.coeffs[j])*(pointX**(self.degree-j-1))
        return finalAns
#trignometry
class sine(Function):
    def __init__(self,  key, category, startCoords, endCoords, showCoords, A, B, C, transformation):
        super().__init__(key, category, startCoords, endCoords, showCoords)
        self.A = A
        self.B = B
        self.C = C
        self.transformation = transformation
    def getCoords(self):
        x = np.arrange(showCoords[0], showCoords[1],0.1)
        y = np.sin(x)
        allCoords = []
        for i in range(len(x)):
            allCoords.append(x[i],y[i])
        return allCoords
    @staticmethod 
    def expression():
        return "Asin(Bx) + C"

    def getDerivative(self,pointX):
        finalAns = self.A*self.B*np.cos(pointX)
        return finalAns

class cos(Function):
    def __init__(self, startCoords, endCoords, showCoords, A, B, C, transformation):
        super().__init__(key, category, startCoords, endCoords, showCoords)
        self.A = A
        self.B = B
        self.C = C
        self.transformation = transformation
    def getCoords(self):
        x = np.arrange(showCoords[0], showCoords[1],0.1)
        y = np.sin(x)
        allCoords = []
        for i in range(len(x)):
            allCoords.append(x[i],y[i])
        return allCoords
    @staticmethod
    def expression():
        return "Acos(Bx) + C"
    def instructions(self):
        return "Please enter the values of A, B, and C"
    def getDerivative(self,pointX):
        finalAns = -self.A*self.B*np.sin(pointX)
        return finalAns

#conic sections
class conic(Function):
    conicsDict = {"Circle" : "(x - a)**2 + (y - b)**2 = r**2",
         "Ellipse": "(x**2/a**2) + (y**2/b**2) = 1"}
    def __repr__(self):
        for key in conicsDict:
            if key == self.key:
                return conicsDict[key]
    def __init__(self, key, category, startCoords, endCoords, showCoords,coeffs, transformation,rolling=False):
        super().__init__(key, category, startCoords, endCoords, showCoords)
        self.key = key
        self.coeffs = coeffs
        self.transformation = transformation
        self.rolling = rolling
    def getCoords(self):
        if (self.key == "circle"):
            x = np.arrange(showCoords[0], showCoords[1],0.1)
            y = []
            for i in range(len(x)):
                tempY = (self.coeffs[2]**2 - (x[i] - self.coeffs[0]**2)) **0.5 + self.coeffs[1]
                y.append(tempY)
            allCoords = []
            for i in range(len(x)):
                allCoords.append(x[i],y[i])
            return allCoords
        if (self.key == "ellipse"):
            x = np.arrange(showCoords[0], showCoords[1],0.1)
            y = []
            for i in range(len(x)):
                tempY = (self.coeffs[0]**2  * (1 - (x[i]/self.coeffs[1])**2))**0.5
                y.append(tempY)
            allCoords = []
            for i in range(len(x)):
                allCoords.append(x[i],y[i])
            return allCoords
    def getDerivative(self,pointX, pointY):
        if (self.key == "circle"):
            try:
                return -(2*(pointX-self.coeffs[0]))/(2*((pointY-self.coeffs[1]) - 1))
            except ZeroDivisionError:
                return None
        else:
            try:
                return -((self.coeffs[1]**2)*pointX)/((self.coeffs[0]**2)*pointY)
            except ZeroDivisionError:
                return None
    
    

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
        self.currFunctionCat = None
        self.currDelete = None
        self.falling = False
        #we only have a certain number of functions
        self.functionsStock = [4]*6
        self.isRunning = False
        self.posX = None
        self.posY = None
        self.feetX = None
        self.feetY = None
        self.name = "player1"
        #states
        self.dead = False
        self.won = False
class Terrain(object):
    def __init__(self, width, height, chunk_size, level):
        #initialisation
        self.spikesLocs = []
        self.starsLocs = []
        self.TNTLocs = []
        self.holes = []
        self.terrainDims = [[width,height]]
        self.run()

    def run(self):
        self.seeds = [15,30,40,50,60,70,80,90,100,110]
        self.textures = [2.5, 2.2, 1.8, 1.6, 1.4, 1.3, 1.2, 1.0, 1.0, 0.9]
        self.num_iterations = [9]*9
        terrainFillRaw = []
        for i in range(len(self.seeds)-5):
            beginCoords = [(100, 500), (1900, 250)]
            terrainFillRaw.append(self.midpointDisplacement(beginCoords, 200, 600, self.textures[i], self.seeds[i], self.num_iterations[i])) 
        self.terrainFills = terrainFillRaw
        self.breaksTot = []
        for i in range(len(self.terrainFills)):
            self.breaksTot.append(self.introduceBreaks(self.terrainFills[i], i+1))

        self.starPos = []
        for i in range(len(self.terrainFills)):
            self.starPos.append(self.placeStars(i+1))
            
    def placeStars(self, level):
        stars_points = []
        stars_points_breaks = []
        displacement = [2, 10, 12, 15, 15]
        inBetweenBreaks = [False, False, True, True, True]
        star_nums = [4, 4, 6, 8,10]
        currTerrain = tuple(self.terrainFills[level-1])
        print(level-1)
        for i in range(len(currTerrain) - 1):
            if inBetweenBreaks[level-1] == False and self.breaksTot[level-1][i] == False: 
                midpointX = (currTerrain[i][0] + currTerrain[i+1][0])/2
                midpointY = (currTerrain[i][1] + currTerrain[i+1][1])/2
                midpointY -= random.choice(displacement[:level])
                stars_points.append([midpointX, midpointY])
            elif inBetweenBreaks[level-1] == True:
                if self.breaksTot[level-1][i] == False:
                    midpointX = (currTerrain[i][0] + currTerrain[i+1][0])/2
                    midpointY = (currTerrain[i][1] + currTerrain[i+1][1])/2
                    midpointY -= random.choice(displacement[:level])
                    stars_points.append([midpointX, midpointY])
                else:
                    midpointX = (currTerrain[i][0] + currTerrain[i+1][0])/2
                    midpointY = (currTerrain[i][1] + currTerrain[i+1][1])/2
                    midpointY -= random.choice(displacement[:level])
                    stars_points_breaks.append([midpointX, midpointY])
        
        if inBetweenBreaks[level-1]:
            return random.sample(stars_points_breaks, star_nums[level-1]//2) + random.sample(stars_points, star_nums[level-1]//2) 
        else:
            return random.sample(stars_points, star_nums[level-1]//2)
       
    def midpointDisplacement(self,beginCoords, minHeight, maxHeight, texture, seed, totIterations):
        startX = beginCoords[0][0]
        startY = beginCoords[0][1]
        endX = beginCoords[1][0]
        endY = beginCoords[1][1]
        #sanitising the texture (put in required range)
        if texture > 3.0:
            texture = 3.0
        elif texture < 0.5:
            texture = 0.5
        #setting an initial displacement
        displacement = (startY + endY)/2
        #segment points list (2D list) with tuples
        seg_points = [[startX, startY], [endX, endY]]
        currIteration = 1
        random.seed(seed)
        while currIteration <= totIterations:
            seg_points_tuple = tuple(seg_points)
            disp_type = random.randint(0,1)
            for i in range(len(seg_points)-1):
                midpointX = (seg_points_tuple[i][0] + seg_points_tuple[i+1][0])/2
                midpointY = (seg_points_tuple[i][1] + seg_points_tuple[i+1][1])/2
                midpoint = [midpointX,midpointY] 
                if disp_type == 0 or disp_type == 1:
                    # Displace midpoint y-coordinate
                    midpoint[1] += random.choice([-displacement,
                                                  displacement])
                    if midpoint[1] > maxHeight:
                        midpoint[1] = maxHeight
                    elif midpoint[1] < minHeight:
                        midpoint[1] = minHeight
                    bisect.insort(seg_points, midpoint)
                else:
                    flag = False
                    if (seg_points_tuple[i+1][0] - seg_points_tuple[i][0] != 0 and seg_points_tuple[i+1][1] - seg_points_tuple[i][1] != 0):
                        gradient = (seg_points_tuple[i+1][1] - seg_points_tuple[i][1])/(seg_points_tuple[i+1][0] - seg_points_tuple[i][0])
                        normalGrad = -1/gradient
                        c = midpointY - (normalGrad*midpointX)
                        change = random.choice([-displacement,displacement])
                        a = 1 + normalGrad**2
                        b = -(2*midpointX) + (2*normalGrad*(c - midpointY))
                        c = (midpointX**2) + (c-midpointX)**2 - (change**2)
                        midPointX = solveQuad(a,b,c)
                        if not isinstance(midPointX, complex):
                            midPointY = (normalGrad * midPointX) + c
                            midpoint = [midPointX, midPointY]
                            flag = True
                            if midpoint[1] > maxHeight:
                                midpoint[1] = maxHeight
                            elif midpoint[1] < minHeight:
                                midpoint[1] = minHeight
                    elif flag == False:
                        # Displace midpoint y-coordinate
                        midpoint[1] += random.choice([-displacement,
                                                      displacement])
                        if midpoint[1] > maxHeight:
                            midpoint[1] = maxHeight
                        elif midpoint[1] < minHeight:
                            midpoint[1] = minHeight
                    bisect.insort(seg_points, midpoint)
            # Reduce displacement range
            displacement *= 2 ** (-texture)
            # update number of iterations
            currIteration += 1
        return seg_points

        """
        while currIteration <= totIterations:
            for i in range(len(seg_points)-1):
                disp_type = random.randint(0,1)
                midpointX = (seg_points[i][0] + seg_points[i+1][0])/2
                midpointY = (seg_points[i][1] + seg_points[i+1][1])/2
                if disp_type == 0 or disp_type == 1:
                    #symmetric bounds used
                    midpointY += random.choice([-displacement,displacement])
                    if midpointY > maxHeight:
                        midpointY = maxHeight
                    elif midpointY < minHeight:
                        midpointX = minHeight
                elif disp_type == 2:
                    if (seg_points[i+1][0] - seg_points[i][0] != 0 and seg_points[i+1][1] - seg_points[i][1] != 0):
                        gradient = (seg_points[i+1][1] - seg_points[i][1])/(seg_points[i+1][0] - seg_points[i][0])
                        normalGrad = -1/gradient
                        c = midpointY - (normalGrad*midpointX)
                        change = random.choice([-displacement,displacement])
                        a = 1 + normalGrad**2
                        b = -(2*midpointX) + (4*(c - midpointY))
                        c = (midpointX**2) + (c**2) - (change**2)
                        midPointX = solveQuad(a,b,c)
                        midPointY = (normalGrad * midPointX) + c
                        if midpointY > maxHeight:
                            midPointY = maxHeight
                        elif midpointY < minHeight:
                            midPointX = minHeight
                midpoint = (midpointX, midpointY)
                bisect.insort(seg_points, midpoint)
            displacement *= 2 ** (-texture)
            currIteration += 1
        return seg_points
        """

    def findCoordinatesBreaks(self, arr, dxLow, dxHigh, dyLow, dyHigh, start, end, level, frame):
        layer = self.terrainFills[level-1]
        ind = 0
        while ind < len(layer):
            transformedX1 = layer[ind][0] - (frame*600)
            flag = False
            if start <= transformedX1 <= end:
                largestI = ind
                for i in range(ind+1, len(layer)):
                    transformedX2 = layer[i][0] - (frame*600)
                    if start <= transformedX2 <= end:
                        if dxLow <= layer[i][0] - layer[ind][0] <= dxHigh:
                            if dyLow <= abs(layer[i][1] - layer[ind][1]) <= dyHigh:
                                arr.append((ind, i))
                                largestI = i
                                flag = True
                                if random.choice([0,1]) == 1:
                                    break
                ind = largestI 
            if flag == False:
                ind += 1
        
        
    def introduceBreaks(self, seg_points, level):
        breaks = [False]*(len(seg_points)-1)
        breaksIndF1 = []
        breaksIndF2 = []
        breaksIndF3 = []
        combBreaks = [breaksIndF1, breaksIndF2, breaksIndF3]
        breaksRange = [[(50,100),(0,40)], [(50,100),(0,40)], [(70,400),(0,100)], [(100,500),(0,100)], [(100,500),(0,200)]]
        #two breaks in the first half, two breaks later
        for i in range(3):
            dxLow = breaksRange[level-1][0][0]
            dxHigh = breaksRange[level-1][0][1]
            dyLow = breaksRange[level-1][1][0]
            dyHigh = breaksRange[level-1][1][1]
            res = self.findCoordinatesBreaks(combBreaks[i], dxLow, dxHigh, dyLow, dyHigh, 150, 650, level, i)
        print(len(breaksIndF1), len(breaksIndF2), len(breaksIndF3), level)
        #select one/two from each of them
        finalBreaks = random.sample(breaksIndF1, 2) + random.sample(breaksIndF2, 1) + random.sample(breaksIndF3, 2)
        
        #fill true for each tuple range
        for (start, end) in finalBreaks:
            for i in range(start, end+1):
                breaks[i] = True
        
        return breaks
           
        
    
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
    def redrawAll(mode,canvas):
        canvas.create_text(mode.width/2, 25, text="Help and Instructions", font="Helvetica 25 bold")
        canvas.create_text(mode.width/2, 400, text="", font="Arial 15")
        
    def keyPressed(mode, event):
        if (event.key == "Left"):
            mode.app.setActiveMode(mode.app.HomeScreenMode)
class StatsScreenMode(Mode):
    def redrawAll(mode, canvas):
        mode.drawStatsScreen(canvas)

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
            return existingFile
        except:
            return None
        

    def drawStatsScreen(mode,canvas):
        playerS = mode.playerStats()
        if  playerS != None:
            pass
        else:
            canvas.create_text(mode.width/2, mode.height/4 - 30, text="Score: 0")
            canvas.create_text(mode.width/2, mode.height/2 - 30, text="Stars: 0")
            canvas.create_text(mode.width/2, 3*mode.height/4 - 30, text="Spikes: 0")
            canvas.create_text(mode.width/2, mode.height - 30, text= "TNTs: 0")

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
        for i in range(1,16):
            print(mode.terrain.terrainFills[mode.player.currLevel-1][-i])
        mode.currPt = 0
        mode.addFrame = [False, False]
        mode.deleteFrame = False
        mode.editFrame = [False, False]
        mode.entered = False

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
        mode.backButton = mode.backButton.resize((50,50))

    def redrawAll(mode, canvas):
        mode.drawLevel(canvas, mode.terrain.terrainFills[mode.player.currLevel-1], mode.terrain.breaksTot[mode.player.currLevel-1], (100,100), (700, 700), mode.colorChoice)
        mode.addGameBar(canvas)
        mode.drawStars(canvas, 15)
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
            if mode.select1 != (-1,-1) and mode.select2 != (-1,-1):
                mode.select1 = (-1,-1)
                mode.select2 = (-1,-1)
            if mode.select1 == (-1,-1):
                mode.select1 = (event.x, event.y)
            elif mode.select2 == (-1,-1):
                mode.select2 = (event.x, event.y)
        if mode.addFrame[0] == True:
            val = mode.checkIfMenu1Pressed(event)
            if val:
                mode.addFrame[0] = False
                mode.addFrame[1] = True
        elif mode.addFrame[1] == True:
            val = mode.checkIfAddButtonPressed(event)
            if val:
                mode.player.functionStock[mode.player.currPlayer[1]] -= 1
                mode.addFunctionToModel()
                mode.addFrame[0] = False
                mode.addFrame[1] = False
    def keyPressed(mode, event):
        if event.key == "s":
            mode.selectionMode = not mode.selectionMode
            if selectionMode == False:
                mode.select1 = mode.select2 = (-1,-1)
        if event.key == "r":
            mode.init = True
        if event.key == "Right" and mode.player.falling == False:
            mode.animate()
            
            
    def drawHighlighterTool(mode,canvas):
        if mode.select1 != (-1,-1): 
            canvas.create_line(mode.select1[0], mode.select1[1],
                               mode.select1[0],100, fill='blue')
        if mode.select2 != (-1,-1):
            canvas.create_line(mode.select2[0], mode.select2[1],
                               mode.select2[0],100, fill='blue')
            
    def drawLevel(mode, canvas, terrainFill, breakPts, startPixel, endPixel, colorChoice):
        canvas.create_rectangle(startPixel[0], startPixel[1], endPixel[0], endPixel[1], fill = colorCode(117, 218, 255))
        colorsDict = {'0': (195, 157, 224), '1': (158, 98, 204),
                          '2': (130, 79, 138), '3': (68, 28, 99), '4': (49, 7, 82),
                          '5': (23, 3, 38), '6': (240, 203, 163)}
        
        colorTup = colorsDict[str(colorChoice)]
        layer = []
        for i in range(mode.startInd, mode.endInd-1):
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
        mode.init = False
        
    def animate(mode):
        mode.setImages()
        if mode.player.posX < 100 and mode.frame == 0:
            mode.player.posX += 10
            now = time.time()
            if now - mode.last_time > 0.05:
                mode.last_time = now
                mode.player.currFrame = (mode.player.currFrame + 1) % 4
        elif mode.player.posX > 700 and mode.frame == 3:
            mode.player.posX += 10
            now = time.time()
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
                if mode.frame == 3:
                    return
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
        print(originalH)
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
        if 20 <= event.y <= 80 and 20 <= event.x <= 80:
            mode.app.setActiveMode(mode.app.HomeScreenMode)
        elif mode.width-125 <= event.x <= mode.width:
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
            mode.app.setActiveMode(mode.app.GameMode2)

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
    
    def parameterEntry(mode, canvas, paramList):
        #title
        canvas.create_text(50, 730, text= mode.player.currFunctionCat,font= "Arial 30 bold")
        #name/key
        rand = random.radint(1,200)
        canvas.create_text(50, 760, text= f'function{rand}',font= "Arial 15 bold")
        #description
        #description = queryDescription(mode.player.currFunction[0])
        #canvas.create_text(30, self.width/2, text= description,font= "Arial 30")
        degree = 1
        if mode.player.currFunctionCat == "Polynomial":
            degree = self.getUserInput("What is the degree of the polynomial?")
            validationFlag = False
            while validationFlag == False:
                try:
                    degree = int(degree)
                    if degree < 6:
                        validationFlag = True
                except:
                    degree = self.getUserInput("What is the degree of the polynomial?")
            mode.player.currFunction = [None, None, None, None, None, [None]*degree, None, degree]
            mode.player.currFunction[0] = f"function{rand}"
            mode.player.currFunction[1] = mode.player.currFunctionCat
            canvas.create_text(50, 780, text= f"Degree: {mode.player.currFunction[7]}",font= "Arial 15 bold")
            params = []
            for i in range(len(degree+1)):
                letter = string.ascii_uppercase[i]
                params.append(letter)
            finalExp = ""
            for i in range(len(params)-1, -1, -1):
                finalExp += f"{params[i]}x**{self.player.currFunction[5] - i - 1}", 
            canvas.create_text(100, 750, text= f"{finalExp}",font= "Arial 15 bold")
            count = 0
            for row in range(3):
                for col in range(2):
                    if count < len(params):
                        canvas.create_text(200 + 50*col, 725 + 25*row, text=f"Change coefficient {params[count]}")
                    count += 1
        elif mode.player.currFunctionCat == "Sine" or mode.player.currFunctionCat == "Cosine":
            mode.player.currFunction = [None, None, None, None, None, None, None, None, None]
            mode.player.currFunction[0] = f"function{rand}"
            mode.player.currFunction[1] = mode.player.currFunctionCat
            if mode.player.currFunctionCat == "Sine":
                canvas.create_text(100, 750, text= sine.expression(),font= "Arial 15 bold")
            else:
                canvas.create_text(100, 750, text= cos.expression(),font= "Arial 15 bold")
                
            params = Function.params[mode.player.currFunctionCat]
            for i in range(len(params)):
                canvas.create_text(400, 350 + i*20, text=f"Change coefficient {params[i]}")
        elif mode.player.currFunctionCat == "Circle" or mode.player.currFunctionCat == "Ellipse":
            mode.player.currFunction = [None, None, None, None, None, None, None, None, None]
            mode.player.currFunction[0] = f"function{rand}"
            mode.player.currFunction[1] = mode.player.currFunctionCat
            params = Function.params[self.player.currFunction.category]
            for i in range(len(params)):
                canvas.create_text(400, 350 + i*20, text=f"Change coefficient {params[i]}")

        canvas.create_text(500, 725, text="Start coordinates. You can represent pi as \"pi\"")
        canvas.create_text(500, 775, text="End coordinates. You can represent pi as \"pi\"")
        createButton(canvas, 550, 750, mode.buttonDim[0][1], mode.buttonDim[0][0], "Add function" , "Arial 15 bold", 'white', pink)
        
    def checkIfMenu2Pressed(mode, event):
        length = 25
        count = 0
        for row in range(3):
            for col in range(2):
                if  (200 + 50*col)-length <= event.x <= (200 + 50*col)+length:
                    if (625 + 25*row)-length <= event.y <= (625 + 25*row)+length:
                        if count < len(mode.currParams):
                            param = mode.getUserInput(f"What is the value of {mode.currParams[count]}?")
                            mode.currFunction[5][count] = param
        if 500 - length <= event.x <= 500 + length and 625 - length <= event.y <= 625 + length:
            x = mode.getUserInput(f"What is the value of start x coordinate?")
            y = mode.getUserInput(f"What is the value of start y coordinate?")
            mode.currFunction[2] = (x,y)
        elif 500 - length <= event.x <= 500 + length and 675 - length <= event.y <= 675 + length:
            x = mode.getUserInput(f"What is the value of end x coordinate?")
            y = mode.getUserInput(f"What is the value of end y coordinate?")
            mode.currFunction[3] = (x,y)

    def addFunctionToModel(mode):
        if mode.player.currFunction[1] == "Polynomial":
            mode.player.myFunctions[mode.currFunction[0]] = polynomial(mode.player.currFunction[0], mode.player.currFunction[1], mode.player.currFunction[2],
                                                                       mode.player.currFunction[3], mode.player.currFunction[4], mode.player.currFunction[5],
                                                                       mode.player.currFunction[6], mode.player.currFunction[7])
        elif mode.player.currFunction[1] == "Sine":
            mode.player.myFunctions[mode.currFunction[0]] = sine(mode.player.currFunction[0], mode.player.currFunction[1], mode.player.currFunction[2],
                                                                       mode.player.currFunction[3], mode.player.currFunction[4], mode.player.currFunction[5][0],
                                                                       mode.player.currFunction[5][1], mode.player.currFunction[5][2], mode.player.currFunction[6])
        elif mode.player.currFunction[1] == "Cosine":
            mode.player.myFunctions[mode.currFunction[0]] = cos(mode.player.currFunction[0], mode.player.currFunction[1], mode.player.currFunction[2],
                                                                       mode.player.currFunction[3], mode.player.currFunction[4], mode.player.currFunction[5][0],
                                                                       mode.player.currFunction[5][1], mode.player.currFunction[5][2], mode.player.currFunction[6])
        elif mode.player.currFunction[1] == "Circle" or mode.player.currFunction[1] == "Ellipse":
            mode.player.myFunctions[mode.currFunction[0]] = conic(mode.player.currFunction[0], mode.player.currFunction[1], mode.player.currFunction[2],
                                                                       mode.player.currFunction[3], mode.player.currFunction[4], mode.player.currFunction[5],
                                                                       mode.player.currFunction[6])
        

    def checkIfMenu1Pressed(mode, event):
        for col in range(6):
            l = 100
            cx = 125 + 100*col
            cy = 750
            if cx - l <= event.x <= cx + l:
                if cy - l <= event.y <= cy + l:
                    mode.player.currFunctionCat = Function.functions[i]
                    return True
        return False
    def checkIfAddButtonPressed(mode, event):
        return checkIfButtonPressed(550, 650, event, mode.buttonDim[0][1], mode.buttonDim[0][0])
        
    def lostGame(mode):
        mode.app.setActiveMode(mode.app.lostGameScreen)
    def wonGame(mode):
        mode.app.setActiveMode(mode.app.wonGameScreen)
        
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
        info = [mode.player.score, mode.player.stars, mode.player.spikes, mode.player.TNTs]
        infoTxt = ["Score", "Stars", "Spikes", "TNTs"]
        for i in range(len(info)):
            canvas.create_text(mode.width, 400 + 25*i, text=f"{infoTxt[i]}: {info[i]}", fill='white', font="Arial 20")
        create_button(canvas, mode.width, 550, buttonsDim[0][1], mode.buttonsDim[0][0], "Restart", "Arial 15 bold", 'white', 'pink')
    def mousePressed(mode, event):
        val = checkIfButtonPressed(mode.width/2, 550, event, mode.buttonDim[0][1], mode.buttonDim[0][0])
        if val:
            mode.app.setActiveMode(mode.app.GameMode1)

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
        info = [mode.player.score, mode.player.stars, mode.player.spikes, mode.player.TNTs]
        infoTxt = ["Score", "Stars", "Spikes", "TNTs"]
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

            
    

def main():
    MyApp(width=800,height=800)

if __name__ == '__main__':
    main()

