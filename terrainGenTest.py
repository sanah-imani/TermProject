
#final terrain generation algorithm:

#Code modified but sourced from: https://github.com/buckinha/DiamondSquare/blob/master/src/hkb_diamondsquare/DiamondSquare.py

import random
import math
import numpy as np

"""
def diamondSquare(shape, min_height, max_height, texture, random_seed=None):

    # sanitize inputs
    if texture > 1:
        texture = 1.0
    if texture < 0:
        texture = 0.0

    finShape, iterations = findShapeAndIterations(shape)

    # create the array
    diamondSquareArr = np.full(finShape, -1)

    # seed the random number generator
    random.seed(random_seed)

    # seed the corners
    diamondSquareArr[0, 0] = random.uniform(0, 1)
    diamondSquareArr[finShape[0] - 1, 0] = random.uniform(0, 1)
    diamondSquareArr[0, finShape[1]-1] = random.uniform(0, 1)
    diamondSquareArr[finShape[0]-1, finShape[1]-1] = random.uniform(0, 1)

    # do the algorithm
    for i in range(iterations):
        r = math.pow(texture, i)

        step = math.floor((finShape[0]-1) / math.pow(2, i))

        diamond_step(diamondSquareArr, step, r)
        square_step(diamondSquareArr, step, r)

    # rescale the array to fit the min and max heights specified
    diamondSquareArr = min_height + (diamondSquareArr * (max_height - min_height))

    # trim array, if needed
    finalArray = diamondSquareArr[:shape[0], :shape[1]]

    return finalArray

def findShapeAndIterations(requested_shape, max_power_of_two=13):
    if max_power_of_two < 3:
        max_power_of_two = 3

    largest_edge = max(requested_shape)

    for power in range(1, max_power_of_two+1):
        d = (2**power) + 1
        if largest_edge <= d:
            return (d, d), power

    #failsafe: no values in the dimensions array were allowed, so print a warning and return
    # the maximum size.
    d = 2**max_power_of_two + 1
    print("DiamondSquare Warning: Requested size was too large. Grid of size {0} returned""".format(d))
    return (d, d), max_power_of_two


def diamond_step(dsArr, step, texture):
    
    # calculate where all the diamond corners are (the ones we'll be filling)
    half_step = math.floor(step/2)
    x_steps = range(half_step, dsArr.shape[0], step)
    y_steps = x_steps[:]

    for i in x_steps:
        for j in y_steps:
            if dsArr[i,j] == -1.0:
                dsArr[i,j] = diamond_displace(dsArr, i, j, half_step, texture)


def square_step(dsArr, step, texture):

    # set the half-step for the calls to square_displace
    half_step = math.floor(step/2)

    # vertical step
    steps_x_vert = range(half_step, dsArr.shape[0], step)
    steps_y_vert = range(0, dsArr.shape[1], step)

    # horizontal step
    steps_x_horiz = range(0, dsArr.shape[0],   step)
    steps_y_horiz = range(half_step, dsArr.shape[1],   step)

    for i in steps_x_horiz:
        for j in steps_y_horiz:
            dsArr[i,j] = square_displace(dsArr, i, j, half_step, texture)

    for i in steps_x_vert:
        for j in steps_y_vert:
            dsArr[i,j] = square_displace(dsArr, i, j, half_step, texture)


def diamond_displace(DS_array, i, j, half_step, roughness):
    
    ul = DS_array[i-half_step, j-half_step]
    ur = DS_array[i-half_step, j+half_step]
    ll = DS_array[i+half_step, j-half_step]
    lr = DS_array[i+half_step, j+half_step]

    ave = (ul + ur + ll + lr)/4.0

    rand_val = random.uniform(0,1)

    return (roughness * rand_val) + (1.0 -roughness) * ave


def square_displace(DS_array, i, j, half_step, roughness):
    _sum = 0.0
    divide_by = 4

    # check cell "above"
    if i - half_step >= 0:
        _sum += DS_array[i-half_step, j]
    else:
        divide_by -= 1

    # check cell "below"
    if i + half_step < DS_array.shape[0]:
        _sum += DS_array[i+half_step, j]
    else:
        divide_by -= 1

    # check cell "left"
    if j - half_step >= 0:
        _sum += DS_array[i, j-half_step]
    else:
        divide_by -= 1

    # check cell "right"
    if j + half_step < DS_array.shape[0]:
        _sum += DS_array[i, j+half_step]
    else:
        divide_by -= 1

    ave = _sum / divide_by

    rand_val = random.uniform(0, 1)

    return (roughness * rand_val) + (1.0-roughness) * ave

print(run(.4, 70))


#figure out if 2D or 3D...sample a 2D slice
def run(self,texture,seed):
    self.seeds = [20,30,40,50,60,70,80,90,100,110]
    self.textures = [3, 2, 1.5, 1.2, 1.0, 1.3, 1.1, 0.9, 1.0, 1.0]
    self.num_iterations = [getIterations(chunk_sizes[i]) for i in range(9)]
    terrainFillRaw = []
    for i in range(len(self.seeds)):
        terrainFillRaw += midpointDisplacement((80,80), 70, 300, self.textures[i], self.seeds[i], self.num_iterations[i])
    self.terrainPixels = terrainFillRaw

import os
import random
import math
from PIL import Image

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
        
        
def _get_working_shape_and_iterations(requested_shape, max_power_of_two=13):
    """Returns the necessary size for a square grid which is usable in a DS algorithm.
    The Diamond Square algorithm requires a grid of size n x n where n = 2**x + 1, for any 
    integer value of x greater than two. To accomodate a requested map size other than these
    dimensions, we simply create the next largest n x n grid which can entirely contain the
    requested size, and return a subsection of it.
    This method computes that size.
    PARAMETERS
    ----------
    requested_shape
        A 2D list-like object reflecting the size of grid that is ultimately desired.
    max_power_of_two
        an integer greater than 2, reflecting the maximum size grid that the algorithm can EVER
        attempt to make, even if the requested size is too big. This limits the algorithm to 
        sizes that are manageable, unless the user really REALLY wants to have a bigger one.
        The maximum grid size will have an edge of size  (2**max_power_of_two + 1)
    RETURNS
    -------
    An integer of value n, as described above.
    """
    if max_power_of_two < 3:
        max_power_of_two = 3

    largest_edge = max(requested_shape)

    for power in range(1, max_power_of_two+1):
        d = (2**power) + 1
        if largest_edge <= d:
            return (d, d), power

    #failsafe: no values in the dimensions array were allowed, so print a warning and return
    # the maximum size.
    d = 2**max_power_of_two + 1
    print("DiamondSquare Warning: Requested size was too large. Grid of size {0} returned""".format(d))
    return (d, d), max_power_of_two




print(run(.7, 70))
