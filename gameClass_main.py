###################################################
#This code has been written by Sanah Imani (simani)
#All commented code may not be fully runnable yet
###################################################
from cmu_112_graphics import *
import os
import time
import random
import math

#import requests
#from bs4 import BeautifulSoup
# other important functions
#Source: https://www.cs.cmu.edu/~112/notes/
#notes-data-and-operations.html#FloatingPointApprox
def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)
"""
#place Stars - self refers to the terrain object
#this is capped at 4 stars per level
def placeStars(self):
    potentialPlaces = []
    for row in range(len(self.terrainFill)):
        for col in range(len(self.terrainFill[0])):
            if self.terrainFill[row][col] == False
                and closeToLand(self, row, col):
                    potentialPlaces.append((row,col))

    if len(potentialPlaces) < 4:
        return potentialPlaces
    else:
        return random.sample(potentialPlaces, 4)

#place spikes:
def placeSpikes(self):
    potentialPlaces = []
    for row in range(len(self.terrainFill)):
        for col in range(len(self.terrainFill[0])):
            if self.terrainFill[row][col] == True and
                closeToAir(self,row,col):
                    potentialPlaces.append((row,col))
    if len(potentialPlaces) < 6:
        return potentialPlaces
    else:
        return random.sample(potentialPlaces,6)
    
#check if character collides into stars
#self refers to the character object
def collideStars(self, starPos):
    starRadius = 10
    for i in range(len(starPos)):
        if distance(starPos[i][0], self.posX) < starRadius
            and distance(starPos[i][1], self.posY) < starRadius:
            starPos.pop(i)
            self.player.score += 10
            self.player.stars += 1
#checking if the player hit a spike
def collideSpike(self, spikePos):
    deletePos = []
    for pointsL in spikePos:
        if pointsL[0] <= self.player.posX <= pointsL[2] and
            points[5] <= self.player.posX <= pointsL[1]:
                ind = spikePos.find(pointsL)
                deletePos.append(ind)
                self.player.spikes += 1
    for ind in deletePos:
        spikePos.pop(ind)
#check if ANYTHING touches TNT
def collideBox(self,boxPos):
    deletePos = []
    #character
    for pointsL in boxPos:
        if pointsL[0] <= self.player.posX <= pointsL[4]
            and pointsL[1] <= self.player.posY <= pointsL[5]:
                ind = boxPos.find(pointsL)
                deletePos.append(ind)
                self.player.TNTs += 1
    for ind in deletePos:
        boxPos.pop(ind)

    deletePos = []
    #functions start and stop points
    
    #function
    for pointsL in boxPos:
        if pointsL[0] <= self.function <= pointsL[4]
            and pointsL[1] <= self.player.posY <= pointsL[5]:
                ind = boxPos.find(pointsL)
                deletePos.append(ind)
                self.player.TNTs += 1
    for ind in deletePos:
        boxPos.pop(ind)
"""
"""
# function definitions
def addFunctionDescription(self, query):
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
"""
class Function(object):
    functions = ['Trignometry', 'Conic Sections', 'Polynomials','Piecewise']
    myFunctions = {}
    params = {'Trignometry': ['A','B', 'C'],
              'Circle': ['a','b','r'],
              'Ellipse': ['a','b'],
              'Polynomials': ['degree'],
              #might remove this 
              'Custom': []
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
    def __init__(self, key, category, startCoords, endCoords, showCoords, degree, coeffs, transformation):
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
    
    def __repr__(self):
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
    def __repr__(self):
        return "Acos(Bx) + C"
    def instructions(self):
        return "Please enter the values of A, B, and C"
    def getDerivative(self,pointX):
        finalAns = -self.A*self.B*np.sin(pointX)
        return finalAns

#conic sections
class conic(Function):
    conicsDict = {"circle" : "(x - a)**2 + (y - b)**2 = r**2",
         "ellipse": "(x**2/a**2) + (y**2/b**2) = 1"}
    def __repr__(self):
        for key in conicsDict:
            if key == self.key:
                return conicsDict[key]
    def __init__(self, startCoords, endCoords, showCoords, key, coeffs, transformation,rolling=False):
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
        self.frames_l = [PhotoImage(file="stickman/stick-L1.gif"),
                         PhotoImage(file="stickman/stick-L2.gif"),
                         PhotoImage(file="stickman/stick-L3.gif"),
                         PhotoImage(file="stickman/stick-L4.gif")]
        self.frames_r = [PhotoImage(file="stickman/stick-R1.gif"),
                         PhotoImage(file="stickman/stick-R2.gif"),
                         PhotoImage(file="stickman/stick-R3.gif"),
                         PhotoImage(file="stickman/stick-R4.gif")]
        """
        self.image = canvas.create_image(WIDTH / 2, HEIGHT-100, anchor=NW,
                                         image=self.frames_l[0])
        self.speedx = 0
        self.speedy = 0
        canvas.bind_all("<KeyPress-Left>", self.move)
        canvas.bind_all("<KeyPress-Right>", self.move)
        canvas.bind_all("<KeyPress-space>", self.jump)
        canvas.bind_all("<KeyRelease-Left>", self.stop)
        canvas.bind_all("<KeyRelease-Right>", self.stop)
        self.current_frame = 0
        self.last_time = time.time()
        """
        self.currLevel = 0
        self.levelsCompleted = []
        self.stars = 0
        self.score = 0
        self.spikes = 0
        self.TNTs = 0
        self.myFunctions = {}
        self.currFunction = None
        self.currDelete = None
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
        self.terrainFill = []
        self.terrainPixels = []
        self.terrainDims = [[width,height]]
        self.setTerrain(self.terrainDims[0][level-1],self.terrainDims[0][level-1], 5)

    def setTerrain(self, width, height, chunk_size):
        numRows = height//chunk_size
        numCols = width//chunk_size
        terrainArr = [([0] * numCols) for row in range(numRows)]
        row = 30 
        for i in range(width//(2*chunk_size)):
            terrainArr[row][i] = 1
        self.terrainPixels += terrainArr
    #figure out if 2D or 3D...sample a 2D slice
def run(self,texture,seed):
    self.seeds = [20,30,40,50,60,70,80,90,100,110]
    self.textures = [3, 2, 1.5, 1.2, 1.0, 1.3, 1.1, 0.9, 1.0, 1.0]
    self.num_iterations = [getIterations(chunk_sizes[i]) for i in range(9)]
    terrainFillRaw = []
    for i in range(len(self.seeds)):
        beginCoords = [(100, random.randint(300,600)), (700, random.randint(300,600))]
        terrainFillRaw += midpointDisplacement(beginCoords, 200, 600, self.textures[i], self.seeds[i], self.num_iterations[i])
    self.terrainPixels = terrainFillRaw

def midpointDisplacement(beginCoords, minHeight, maxHeight, texture, seed, totIterations):
    startX = beginCoords[0][0]
    startY = beginCoords[0][1]
    endX = beginCoords[0][0]
    endY = beginCoords[0][1]
    #sanitising the texture (put in required range)
    if texture > 3.0:
        texture = 3.0
    elif texture < 0.5:
        texture = 0.5
    #setting an initial displacement
    displacement = (startY + endY)/2
    #segment points list (2D list) with tuples
    seg_points = [beginCoords[0], beginCoords[1]]
    currIteration = 0
    random.seed(seed)
    while currIteration <= totIterations:
        for i in range(len(seg_points)-1):
            disp_type = random.randint(0,1)
            midpointX = seg_points[i][0] + seg_points[i+1][0]
            midpointY = seg_points[i][1] + seg_points[i+1][1]
            if disp_type == 0:
                #symmetric bounds used
                midpointY += random.uniform(-displacement,displacement)
                if midpointY > maxHeight:
                    midPointY = maxHeight
                elif midPoint < minHeight:
                    midPointX = minHeight
            else:
                gradient = (seg_points[i+1][1] - seg_points[i][1])/(seg_points[i+1][1] - seg_points[i][0])
                normalGrad = -1/gradient
                c = midpointY - (normalGrad*midpointX)
                change = random.uniform(-displacement,displacement)
                a = 1 + normalGrad**2
                b = -(2*midpointX) + (4*(c - midpointY))
                c = (midpointX**2) + (c**2) - (change**2)
                midPointX = solveQuad(a,b,c)
                midPointY = (normalGrad * x) + c
                if midpointY > maxHeight:
                    midPointY = maxHeight
                elif midPoint < minHeight:
                    midPointX = minHeight
            midpoint = (midPointX, midPointY)
            bisect.insort(seg_points, midpoint)
            
        vertical_displacement *= 2 ** (-texture)
        iteration += 1
    return seg_points

    def colorCode(r,b,g):
        colorval = "#%02x%02x%02x" % (r, g, b)
        return colorval

    def solveQuad(a,b,c):
        discriminant = ((b**2 - 4*a*c)**0.5)
        x1 = (-b + disc)/(2*a)
        x2 = (-b - disc)/(2*a)
        return random.choice([x1, x2])
    
    def drawLandscape(self, canvas, terrainFill, startPixel, endPixel):
        canvas.create_rectangle(startPixel[0], startPixel[1], endPixel[0], endPixel[1], fill = colorCode(87, 156, 208))
        colorsDict = {'0': (195, 157, 224), '1': (158, 98, 204),
                          '2': (130, 79, 138), '3': (68, 28, 99), '4': (49, 7, 82),
                          '5': (23, 3, 38), '6': (240, 203, 163)}
        colorChoice = random.randint(0,6)
        colorTup = colorsDict[str(colorChoice)]
        layer = []
        for i in range(len(terrainFill)-1):
            layer += [terrainFill[i]]
            if layer[i+1][0]-layer[i][0] > 2:
                m = float(terrainFill[i+1][1]-terrainFill[i][1])/(terrainFill[i+1][0]-terrainFill[i][0])
                n = terrainFill[i][1]-m*terrainFill[i][0]
                r = lambda x: m*x+n  # straight line
                for j in range(terrainFill[i][0]+2, terrainFill[i+1][0],2): 
                    layer += [(j, r(j))]
        for (x, y) in layer:
            canvas.create_line(x, y, x, self.terrain.bottom[1], fill=colorCode(colorTup[0], colorTup[1], colorTup[2]), width = 2)

    
class MyApp(App):
    def appStarted(self):
        #canvas dims
        self.width = 800
        self.height = 800
        #add a select coordinates marker
        self.selectC1 = (-1,-1)
        self.selectC2 = (-1,-1)
        #create a player
        
        #exiting a screen flag
        self.exit = False
        #frames dictory
        self.frames = {
            'home': [True, False, False],
            'function': [False, False, False],
            'gameMode': [False, False, False],
            'help': False,
            'statistics': False,
            'share': False
            'select': False}
        
        #important variables
        self.buttonDim = [[120, 60]]
        self.levels = []

        #getting the images ready
        self.setImages()
        #getting the Player
        myPlayer = Player()
        self.player = myPlayer
        
        #getting the terrain ready
        myTerrain = Terrain(400, 400, 5, self.player.currLevel)
        self.terrain = myTerrain
        
        
    #####
    #For debugging purposes: Random set terrain
    #######
    def drawLevel(self, canvas, level):
        for i in range(len(self.terrain.terrainPixels)):
            for j in range(len(self.terrain.terrainPixels[0])):
                if self.terrain.terrainPixels == 1:
                    r = chunk_size//2
                    (x0, y0, x1, y1) = self.getCellBounds(i, j, numRows, numCols, 200)
                    cx = (x0 + x1)//2
                    cy = (y0 + y1)//2
                    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill='green',width=0)
                
         #############################################################################
        #Src: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        ############################################################################
    def getCell(self, x, y, numRows, numCols, margin):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self.pointInGrid(x, y,margin)):
            return (-1, -1)
        gridWidth  = self.width - 2*margin
        gridHeight = self.height - 2*margin
        cellWidth  = gridWidth / numRows
        cellHeight = gridHeight / numCols
        row = int((y - margin) / cellHeight)
        col = int((x - margin) / cellWidth)
        return (row, col)
    
    def getCellBounds(self, row, col, numRows, numCols,margin):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = self.width - 2*margin
        gridHeight = self.height - 2*margin
        cellWidth = gridWidth / numRows
        cellHeight = gridHeight / numCols
        x0 = margin + col * cellWidth
        x1 = margin + (col+1) * cellWidth
        y0 = margin + row * cellHeight
        y1 = margin + (row+1) * cellHeight
        return (x0, y0, x1, y1)

    def pointInGrid(self, x, y,margin):
        # return True if (x, y) is inside the grid defined by app.
        return ((margin <= x <= self.width-margin) and
                (margin <= y <= self.height-margin))
    #######################################################################
    def setImages(self):
        path = 'skyBack.png'
        self.image1 = self.loadImage(path)
        self.image1 = self.image1.resize((self.width, self.height))
        path = 'Logo.png'
        self.image2 = self.loadImage(path)
        self.image2 = self.image2.resize((self.width//2, self.height//4))
        path = 'homeMenu/'
        ind = 0
        self.imagesHome = []
        for file in sorted(os.listdir(path)):
            img = self.loadImage("homeMenu/" + file)
            img = img.resize((self.width//3,self.width//3))
            self.imagesHome.append(img)
        iconPath = 'gameBar/'
        self.imagesBar = []
        for file in sorted(os.listdir(iconPath)):
            img = self.loadImage(iconPath + file)
            img = img.resize((60, 60))
            self.imagesBar.append(img) 
    def checkButtonPressed(self,cx, cy, event, height, width):
        print(cx - (width/2), cx + (width/2), cy-(height/2), cy+(height/2))
        if ((cx - (width/2) <= event.x <= cx+(width/2))
            and (cy-(height/2) <= event.y <= cy+(height/2))):
            return True
        return False

    def generateLevels(self):
        roughness = [0.2, 0.3, 0.3, 0.4, 0.4, 0.4, 0.5, 0.6, 0.8]
        seeds = [20,30,40,50,60,70,80,90,100]
        for i in range(9):
            self.levels.append(self.run(roughness[i], seeds[i]))

    def drawHomeMenu(self,canvas):
        canvas.create_rectangle(0,0,self.width,self.height)
        positions = [((self.width/3 - self.width/6),(self.height/2 + self.height/4)),
                     ((self.width/3 + self.width/6), (self.height/2 - self.height/4)),
                     ((2*self.width/3 + self.width/6), (self.height/2 + self.height/4))]
        ind = 0
        for (cx,cy) in positions:
            canvas.create_image(cx, cy,
                            image=ImageTk.PhotoImage(self.imagesHome[ind]))
            ind += 1
        canvas.create_text(positions[0][0], self.width-50, text="Help", font= "Arial 15 bold")
        canvas.create_text(positions[2][0], self.width-50, text="My Performance", font= "Arial 15 bold")

    def drawHelpMenu(self,canvas):
        canvas.create_text(self.width/2, 25, text="Help and Instructions", font="Helvetica 25 bold")
        canvas.create_text(self.width/2, 400, text="", font="Arial 15")
    
    #save player stats
    def playerStats(player, functions):
        #path to player stats
        playerStatsP = "stats.csv"
        if len(functions) < 3:
            player.score += 10
        if player.stars > 3:
            player.score += 10
        with open(playerStatsP, 'r') as file:
            reader = csv.reader(file)
            existingFile = []
            for row in reader:
                existingFile.append(row)
            
        with open(playerStatsP, 'w') as file:
            writer = csv.writer(file)
            writer.writerow([str(i) for i in range(1,10)])
            #levels completed
            existingFile[1][player.currLevel-1] = True
            writer.writerow(existingFile[1])
            #score
            existingFile[2][player.currLevel-1] = player.score
            writer.writerow(existingFile[2])
            #stars collected
            existingFile[3][player.currLevel-1] = player.stars
            writer.writerow(existingFile[3])
            #no of functions
            existingFile[4][player.currLevel-1] = len(Function.functions)
            writer.writerow(existingFile[4])
    def drawStatsScreen(self,canvas):
        canvas.create_text(self.width/2, self.height/4 - 30, text="Score: 0")
        canvas.create_text(self.width/2, self.height/2 - 30, text="Stars: 0")
        canvas.create_text(self.width/2, 3*self.height/4 - 30, text="Spikes: 0")
        canvas.create_text(self.width/2, self.height - 30, text= "TNTs: 0")
    def checkHomeMenuClicked(self,event):
        positions = [((self.width/3 - self.width/6),(self.height/2 + self.height/4)),
                     ((self.width/3 + self.width/6), (self.height/2 - self.height/4)),
                     ((2*self.width/3 + self.width/6), (self.height/2 + self.height/4))]
        s = self.width/3
        ind = 0
        print(event.x,event.y)
        for (cx, cy) in positions:
            if (cx-s//2) <= event.x <= (cx+s//2) and (cy - s//2) <= event.y <= (cy + s//2):
                if ind == 0:
                    self.frames['help'] = True
                    return True
                elif ind == 2:
                    self.frames['statistics'] = True
                    return True
                else:
                    self.frames['gameMode'][0] = True
                    return True
            ind += 1
        return False
        
    def levelMenu(self, canvas):
        tempImage = self.imagesBar[0]
        tempImage = tempImage.resize((25,25))
        canvas.create_image(25,25,image=ImageTk.PhotoImage(tempImage))
        index = 0
        margin = 50
        for row in range(3):
            for col in range(3):
                if index + 1 in self.player.levelsCompleted:
                    (x0, y0, x1, y1) = self.getCellBounds(row, col,3,3,margin)
                    canvas.create_rectangle(x0, y0, x1, y1,outline='black')
                    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f"{index + 1}", font = "Helvetica 20 bold", fill='black')
                    index += 1

        positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        #add the next level
        if (len(self.player.levelsCompleted) == 0):
            nextLevel = 1
            (x0, y0, x1, y1) = self.getCellBounds(positions[nextLevel-1][0], positions[nextLevel-1][1],3,3,margin)
            canvas.create_rectangle(x0, y0, x1, y1,outline='black')
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f"{nextLevel}",fill='black')
        elif self.player.levelsCompleted[-1] + 1 < 10:
            nextLevel = self.player.levelsCompleted[-1] + 1
            (x0, y0, x1, y1) = self.getCellBounds(positions[nextLevel-1][0], positions[nextLevel-1][1],3,3,margin)
            canvas.create_rectangle(x0, y0, x1, y1,outline='black')
            canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f"{nextLevel}",fill='black')
    def addGameBar(self,canvas):
        canvas.create_rectangle(0,0,self.width,100,fill='pink',width=6)
        #iconHolder
        margin = 50
        for i in range(len(self.imagesBar)):
            canvas.create_image(i*60 + margin, 50, image=ImageTk.PhotoImage(self.imagesBar[i]))
        canvas.create_text(self.width-100, 25, text=f"{self.player.name}")
        canvas.create_text(self.width-50,25, text=f"Score: {self.player.score}")
        canvas.create_text(self.width-100,50, text=f"Stars: {self.player.stars}")
        canvas.create_text(self.width-50,50, text=f"TNT: {self.player.TNTs}")
        
    def functionMenu(self,canvas):
        index = 0
        margin = 50
        for row in range(3):
            for col in range(2):
                (x0, y0, x1, y1) = getCellBounds(self, row, col,3,2,margin)
                canvas.create_rectangle(x0, y0, x1, y1,outline='black')
                canvas.create_text((x0+x1)/2, (y0+y1)/2,text=Function.function[index],fill='black')
                if self.player.functionsStock[index] == 0:
                    canvas.create_text((x0+x1)/2, (y0+y1)/2 - margin/2,text= "None Remaining",fill='black')
                index += 1
                
    def drawTerrain(self,canvas):
        self.addGameBar(canvas)
        self.drawLevel(canvas, self.player.currLevel)
    def drawStars(self, canvas, finalLocs, numRows, numCols, r):
        for (row,col) in finalLocs:
            (x0,y0,x1,y1) = getCellBounds(self,row,col, numRows, numCols, 0)
            center_x = (x0 + x1)/2
            center_y = (y0 + y1)/2
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
    def drawSpikes(self,canvas, finalLocs, numRows, numCols, s):
        for (row,col) in finalLocs:
            (x0,y0,x1,y1) = getCellBounds(self,row,col, numRows, numCols, 0)
            center_x = (x0+x1)/2
            points = [x0,y1,x1,y1,center-x,y0]
            canvas.create_polygon(points, outline='black',width=0,fill='grey')
    def drawTNT(self,canvas, finalLocs, numRows, numCols, l):
        for (row,col) in finalLocs:
            (x0,y0,x1,y1) = getCellBounds(self,row,col, numRows, numCols, 0)
            points = [x0,y0,x0,y1,x1,y1,x1,y0]
            canvas.create_polygon(points,outline='black',width=2)
            center_x = (x0 + x1)/2
            center_y = (y1 + y0)/2
            canvas.create_text(center_x,center_y,text="TNT",font="Arial 8 bold")
        
    def pickEntrance(self):
        originalH = (400 - self.terrain.terrainPixels[0]) + 200
        self.player.posX = 100
        self.player.feetY = originalH-2
    def drawEntrance(self,canvas):
        canvas.create_line(0, originalH, 200, originalH, width = 7, fill="black")
        #setting the position of the character
        width, height = self.player.charFrames[0].size
        canvas.create_image(self.powerX, self.player.feetY - width/2, image = ImageTk.PhotoImage(self.player.charFrames[0]))
    def pickTarget(self):
        finalH = self.terrain.terrainPixels[-1]
        self.terrain.targetH = finalH

    def drawTarget(self, canvas):
        canvas.create_rectangle(700, self.terrain.targetH-50, 800, self.terrain.targetH, width = 6, fill="gold")
        canvas.create_text(750, self.terrain.targetH-25, text="TARGET", font="Arial 15 bold")
    def checkIfWon(self):
        if self.width-50 <= self.posX <= self.width:
            self.player.won = True
    
    def checkIfGameOver(self):
        if collidesWithSpike(self) or collideWithTNT(self) or cannotMove(self) or fallDown(self):
            self.player.dead = True
            
        
            
    def keyPressed(self, event):
        if (event.key == "Left"):
            if self.frames['statistics'] or self.frames['help']:
                self.frames['home'][1] = True
                self.frames['statistics'] = False
                self.frames['help'] = False
        if (self.frames['gameMode'][1] or self.frames['gameMode'][2]):
            if event.key == 's':
                self.frames['select'] = True
        #hiding the selections
        if (self.frames['gameMode'][1] or self.frames['gameMode'][2]):
            if event.key == 'h':
                self.frames['select'] = False
        if (self.frames['gameMode'][2]):
            if (event.key == "Right"):
                (row, col) = self.getCellBounds(self.player.posX, self.player.posY,200)
                #tbd
                pass
        

    def redrawAll(self, canvas):
        if self.frames['home'][0]:
            self.drawSplashScreen(canvas)
        elif self.frames['home'][1]:
            self.drawHomeMenu(canvas)
        elif self.frames['help']:
            self.drawHelpMenu(canvas)
        elif self.frames['statistics']:
            self.drawStatsScreen(canvas)         
        elif self.frames['function'][0] == True:
            if self.currFunction == None:
                self.functionMenu(canvas)
            else:
                self.parameterEntry(canvas)
        elif  self.frames['function'][1] == True:
            self.drawDeleteFunctions(canvas)
        elif self.frames['function'][2] == True:
            self.idEdit = canvas.create_window(300,300)
        if self.frames['gameMode'][0]:
            self.levelMenu(canvas)
        elif self.frames['gameMode'][1]:
            self.drawTerrain(canvas)
            if self.frames['selectMode']:
                self.drawHighlighterTool(canvas)
        elif self.frames['gameMode'][2]:
            self.drawTerrain(canvas)
        """
        if self.player.dead == True:
            self.restartLevel(canvas)
        elif self.player.won == True:
            self.newLevel(canvas)
        """

    def drawHighlighterTool(self,canvas):
        if self.coords1 != (-1,-1): 
            canvas.create_line(self.coords1[0], self.coords1[1],
                               self.coords1[0],0, fill='blue')
        if self.coords2 != (-1,-1):
            canvas.create_line(self.coords2[0], self.coords2[1],
                               self.coords2[0],0, fill='blue')
    def parameterEntry(self, canvas):   
        #title
        canvas.create_text(125, self.width/2, text=f'{self.player.currFunction[0]}',font= "Arial 30 bold")
        #description
        #description = queryDescription(self.player.currFunction.key)
        #canvas.create_text(30, self.width/2, text= description,font= "Arial 30")
        canvas.create_text(200, self.width/2, text= "Click on the text to change the value",font= "Arial 15")
        #only completed for polynomial yet
        if self.player.currFunction.category == "Polynomial":
            degree = self.getUserInput("What is the degree of the polynomial?")
            validationFlag = False
            while validationFlag == False:
                try:
                    degree = int(degree)
                    if degree < 6:
                        validationFlag = True
                except:
                    degree = self.getUserInput("What is the degree of the polynomial?")
            canvas.create_text(250, self.width/2, text= "Degree: self.player.currFunction[5]",font= "Arial 15 bold")
            params = []
            for i in range(len(degree+1)):
                letter = string.ascii_uppercase[i]
                params.append(letter)
            finalExp = ""
            for i in range(len(params)-1, -1, -1):
                finalExp += f"{params[i]}x**{self.player.currFunction[5] - i - 1}", 
            canvas.create_text(300, self.width/2, text= f"{finalExp}",font= "Arial 20 bold")
            for i in range(len(params)):
                canvas.create_text(400, 350 + i*20, text=f"Change coefficient {params[i]}")
        elif self.player.currFunction.category == "Trignometry":
            subcategory = self.getUserInput("Choose between sine and cos. Type 's' for sine and 'c' for cos.")
            validationFlag = False
            while subcategory != 's' and subcategory != 'c':
                subcategory = self.getUserInput("Choose between sine and cos. Type 's' for sine and 'c' for cos.")
            params = Function.params[self.player.currFunction.category]
            for i in range(len(params)):
                canvas.create_text(400, 350 + i*20, text=f"Change coefficient {params[i]}")
        elif self.player.currFunction.category == "Circle" or self.player.currFunction.category == "Ellipse":
            params = Function.params[self.player.currFunction.category]
            for i in range(len(params)):
                canvas.create_text(400, 350 + i*20, text=f"Change coefficient {params[i]}")

        canvas.create_text(300, 350 + (len(params)-1)*20, text="Start coordinates. You can represent pi as \"pi\"")
        canvas.create_text(500, 350 + (len(params)-1)*20, text="End coordinates. You can represent pi as \"pi\"")
            
            
                
        
    def mousePressed(self, event):
         if self.frames['home'][0] == True:
            val = self.checkButtonPressed(400, 600, event, self.buttonDim[0][1], self.buttonDim[0][0])
            if val:
                self.frames['home'][0] = False
                self.frames['home'][1] = True
                name = self.getUserInput('What is your name?')
                if (name != None):
                    self.player.name = name
                else:
                    self.player.name = "player1"
         elif self.frames['home'][1] == True:
             val = self.checkHomeMenuClicked(event)
             if val:
                 self.frames['home'][1] = False
         elif self.frames['function'][0] == True:
            positions = [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1)]
            (row, col) = self.getCell(event.x, event.y, 3, 2, 50)
            if (row,col) != (-1,-1):
                for (rowF,colF) in positions:
                    if (rowF,colF) == (row,col):
                        ind = positions.index((rowF,colF))
                        self.currFunction = [f'function{len(self.myFunctions)}', Function.functions[ind]]
            if (row, col) == (-1,-1):
                if 0 <= event.x <= 30 and 100 <= event.y <= 130:
                    if self.currFunction != None:
                        self.currFunction = None
                    else:
                        self.frames['function'][0] = False
            if self.currFunction != None:
                self.checkIfMenuPressed()
                val = self.checkIfButtonPressed()
                if val:
                    self.player.myFunctions[self.currFunction[0]] = Function(self.player.currFunction[0], self.player.currFunction[1],
                                                                      self.player.currFunction[2], self.player.currFunction[3], self.player.currFunction[4], self.currFunction[5]) 
         elif self.frames['function'][1] == True:
            (row,col) = self.getCell(event.x, event.y, len(self.myFunctions), 1, 150)
            if (row,col) != (-1,-1):
                for (rowF,colF) in positions:
                    if (rowF,colF) == (row,col):
                        ind = positions.find((rowF,colF))
                        self.editFunction(Functions.functions[ind])
            self.checkIfDeletePressed()
            val = self.checkIfButtonPressed()
            if val:
                self.frames['function'][1] = False
                self.frames['gameMode'][1] = True
        
         elif self.frames['function'][2] == True:
            (row,col) = self.getCell(event.x, event.y, len(Function.myfunctions), 1, 150)
            if (row,col) != (-1,-1):
                for (rowF,colF) in positions:
                    if (rowF,colF) == (row,col):
                        ind = positions.find((rowF,colF))
                        temp = Functions.myfunctions.pop(ind)
                        if self.player.currFunction == temp:
                            self.player.currFunction = None
         elif self.frames['share']:
            #check this again
            snap = self.getSnapshot(app)
            self.saveSnapshot()
         elif self.frames['gameMode'][0] == True:
             val = self.checkIfLevelPressed(event)
             if val:
                 self.frames['gameMode'][1] = True
                 self.frames['gameMode'][0] = False
         elif self.frames['gameMode'][1]:
             #val = (close, change name, add, delete, edit, run)
             val = self.checkIfGameBarPressed(event)
             if val[0]:
                 self.frames['gameMode'][1] = False
                 self.frames['gameMode'][0] = True
             elif val[1]:
                 name = self.getUserInput('What is your name?')
                 if (name != None):
                     self.player.name = name
             elif val[2]:
                 self.frames['function'][0] = True
             elif val[3]:
                 self.frames['function'][1] = True
             elif val[4]:
                 self.frames['function'][2] = True
             elif val[5]:
                 self.frames['gameMode'][2] = True
                 self.frames['gameMode'][1] = False
                
                
    def checkIfGameBarPressed(self,event):
        if 20 <= event.y <= 80 and 20 <= event.x <= 80:
            return [True, False, False, False, False, False]
        elif self.width-125 <= event.x <= self.width:
            return [False, True, False, False, False, False]
        elif 20 <= event.y <= 80 and 80 <= event.x <= 140:
            return [False, False, True, False, False, False]
        elif 20 <= event.y <= 80 and 140 <= event.x <= 200:
            return [False, False, False, True, False, False]
        elif 20 <= event.y <= 80 and 200 <= event.x <= 260:
            return [False, False, False, True, False, False]
        elif 20 <= event.y <= 80 and 260 <= event.x <= 320:
            return [False, False, False, False, True, False]
        elif 20 <= event.y <= 80 and 320 <= event.x <= 380:
            return [False, False, False, False, False, True]
        return [False, False, False, False, False, False]
    def checkIfLevelPressed(self,event):
        if 0 <= event.x <= 50 and 0 <= event.y <= 50:
            self.frames['home'][1] = True
            self.frames['gameMode'][0] = False
            return False
        else:
            positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
            (row,col) = self.getCell(event.x,event.y,3,3,50)
            if (row,col) != (-1,-1):
                for (rowL,colL) in positions:
                    if (rowL,colL) == (row,col):
                        ind = positions.index((rowL,colL))
                        self.player.currLevel = ind + 1
                        return True
        return False

    def functionMenu(self,canvas):
        index = 0
        margin = 50
        for row in range(3):
            for col in range(2):
                (x0, y0, x1, y1) = getCellBounds(self, row, col,3,2,margin)
                canvas.create_rectangle(x0, y0, x1, y1,outline='black')
                canvas.create_text((x0+x1)/2, (y0+y1)/2,text=Function.function[index],fill='black')
                if self.player.functionsStock[index] == 0:
                    canvas.create_text((x0+x1)/2, (y0+y1)/2 - margin/2,text= "None Remaining",fill='black')
                index += 1

    def drawSplashScreen(self,canvas):
        canvas.create_image(self.width/2, self.height/2,
                            image=ImageTk.PhotoImage(self.image1))
        self.createButton(canvas, 400, 600, self.buttonDim[0][1], self.buttonDim[0][0], "Play Now!", 'Arial 15 bold', 'white', 'pink')
        canvas.create_image(self.width/2, self.height/3, image=ImageTk.PhotoImage(self.image2))

    def createButton(self, canvas, cx, cy, height,width, text, font, txtC, buttonC):
        canvas.create_rectangle(cx-(width/2), cy-(height/2), cx+(width/2), cy+(height/2), fill=buttonC)
        canvas.create_text(cx, cy, text= text, fill=txtC, font = font)


    def checkIfButtonPressed(self, event):
        if (400 - (width/2) <= event.x <= 400 + (width/2)) and
            (450 - height/2) <= event.y <= (450 - height/2):
                return True
        return False
    def functionEditor(self,canvas):
        #title
        canvas.create_text(15, self.width/2, text=f'{self.player.currFunction.key}',font= "Arial 30 bold")
        #description
        description = queryDescription(self.player.currFunction.key)
        canvas.create_text(30, self.width/2, text= description,font= "Arial 30")
        #params and editing
        if self.player.currFunction.key != "piecewise":
            params = Functions.params[self.player.currFunction.name]
            for i in range(len(params)):
                self.create_text(self.width/2-25, 55 + i*20, text=f'{params[i]}')
                self.round_rectangle(canvas, self.width/2 + 25, 45 + i*20, self.width/2+40, 60 + i*20, 15)
        self.createButton(canvas, 400, 450, self.buttonDims[0][1], self.buttonDims[0][0], "Add function", "Arial 15 bold",
                          "white", "black")
    def drawStars(self, canvas, finalLocs, numRows, numCols, r):
        for (row,col) in finalLocs:
            (x0,y0,x1,y1) = getCellBounds(self,row,col, numRows, numCols, 0)
            center_x = (x0 + x1)/2
            center_y = (y0 + y1)/2
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

    #player dead = restart Level
    def restartLevel(self, canvas):
        if self.player.dead == True:
            canvas.create_rectangle(0,0,self.width,self.height,fill="black")
            canvas.create_text(self.width//2, self.height//2, text = "Sorry try again",
                               color="white", font= "Helvetica 30 bold")
            self.createButton(canvas, (self.width//2), (self.height//2 + 75), self.buttonsDim[0][0],
                              self.buttonsDim[0][1], "Restart", 'Arial 30 bold', 'white', 'pink')
    #player won = new level
    def newLevel(self,canvas):
        if self.player.won:
            if self.player.currLevel < 10:
                canvas.create_rectangle(0,0,self.width,self.height,fill="black")
                canvas.create_text(self.width//2, self.height//2, text = "Level Completed",
                                   color="white", font="Helvetica 30 bold")
                canvas.create_text(self.width//2, (self.height//2 + 30),
                                   text = f'Score: {self.player.score}, Stars: {self.player.stars}, Spikes: {self.player.spikes}',
                                   color="white", font="Helvetica 30 bold")
                self.createButton(canvas, (self.width//2), (self.height//2 + 75), self.buttonsDim[0][0],
                                  self.buttonsDim[0][1], "Restart", 'Arial 30 bold', 'white', 'pink')
            else:
                canvas.create_rectangle(0,0,self.width,self.height,fill="black")
                canvas.create_text(self.width//2, self.height//2, text = "Level Completed",
                                   color="white", font="Helvetica 30 bold")
                canvas.create_text(self.width//2, (self.height//2 + 30),
                                   text = f'Score: {self.player.score}, Stars: {self.player.stars}, Spikes: {self.player.spikes}',
                                   color="white", font="Helvetica 30 bold")
                self.createButton(canvas, (self.width//2), (self.height//2 + 75), self.buttonsDim[0][0],
                                  self.buttonsDim[0][1], "Complete Game", 'Arial 30 bold', 'white', 'pink')

"""
         def checkWon(self):
             if almostEquals(self.player.posX , self.terrain.targetX)
                and almostEquals(self.player.posY, self.terrain.targetY):
                    self.player.won = True
                    self.player.levelsCompleted += [self.player.currLevel]
                    self.player.currLevel +=1 
    
         def keyPressed(app,event):
            if (event.key == "s"):
                self.selectMode = True
            if (event.key == "r"):
                self.flagR = True

                

"""

"""
     if self.player.won:
        if self.checkButtonPressed(event, self.width/2, self.width/2 + 75,
                                   buttonDims[0][1], buttonsDims[0][0]):
            if self.player.currLevel < 10:
                self.frames['gameMode'][0] = True
            else:
                self.frames['home'][1] = True
            
     elif self.player.dead:
        if self.checkButtonPressed(event, self.width/2, self.width/2 + 75,
                                   buttonDims[0][1], buttonsDims[0][0]):
            self.frames['gameMode'][1] = True
"""



def main():
    MyApp(width=800,height=800)

if __name__ == '__main__':
    main()

