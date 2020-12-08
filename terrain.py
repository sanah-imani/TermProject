#terrain generation class
import random
import bisect
import numpy as np
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
        self.textures = [2.5, 2.2, 1.8, 1.0, 1.4, 1.3, 1.2, 1.0, 1.0, 0.9]
        self.num_iterations = [10, 10, 8, 6, 7, 7, 7, 7, 7]
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
        for i in range(len(self.terrainFills)):
            self.spikesLocs.append(self.initialiseSpikesLocs(self.terrainFills[i], i+1))
            
    def placeStars(self, level):
        stars_points = []
        stars_points_breaks = []
        displacement = [2, 10, 12, 15, 15]
        inBetweenBreaks = [False, False, True, True, True]
        star_nums = [4, 4, 6, 8,10]
        currTerrain = tuple(self.terrainFills[level-1])
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
        #select one/two from each of them
        finalBreaks = random.sample(breaksIndF1, 2) + random.sample(breaksIndF2, 1) + random.sample(breaksIndF3, 2)
        
        #fill true for each tuple range
        for (start, end) in finalBreaks:
            for i in range(start, end+1):
                breaks[i] = True
        
        return breaks

    def initialiseSpikesLocs(self, seg_points, level):
        quant = [2,2,2,3,3,3,4,4,4]
        length = [5,5,5,10,10,10,15,15,15]
        spikesLocF1 = []
        spikesLocF2 = []
        spikesLocF3 = []
        combSpikes = [spikesLocF1, spikesLocF2, spikesLocF3]
        for i in range(3):
            self.findSpikesInd(combSpikes[i], seg_points, quant[level-1], length[level-1], i)
        return spikesLocF1 + spikesLocF2 + spikesLocF3
        
    def findSpikesInd(self, spikesInd, seg_points, quant, length, frame):
        count = 0
        trial = 0
        while count <= quant:
            flag = True 
            endInd = self.getEndInd(seg_points, frame)
            rand = random.randint(5, endInd-5)
            if rand not in spikesInd:
                transformedX1 = seg_points[rand][0] - (frame*600)
                if 150 <= transformedX1 <= 650:
                    spikesInd += [rand+i for i in range(length)]
                    count += 1
                    flag = False
            trial += 1
            if flag:
                trial += 1
                if trial > 5:
                    break
    
        return spikesInd

    def getEndInd(self, seg_points, frame):
        res = 0
        for i in range(len(seg_points)):
            transformedX1 = seg_points[i][0] - (frame*600)
            if 150 <= transformedX1 <= 650:
                res = i
        return res


