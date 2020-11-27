#terrain generation
scl = 20
canW = 600
canH = 600
params = {'rows': canH/scl, 'cols': canW/scl}



import random
import math

random.seed(0)


class Terrain(object):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.w = 
    
def generateWhiteNoise(width,height):
    noise = [[r for r in range(width)] for i in range(height)]

    for i in range(0,height):
        for j in range(0,width):
            noise[i][j] = random.randint(0,1)

    return noise

noise = generateWhiteNoise(50,12)



colors = {
    0: 'blue',
    1: 'yellow',
    20: 'green',
    25: 'gray',
    1000: 'white'
    }


noise1 = perlin.noise(width / n1div, length / n1div) # landmass / mountains
noise2 = perlin.noise(width / n2div, length / n2div) # boulders
noise3 = perlin.noise(width / n3div, length / n3div) # rocks



def color(a, b, c): # check land type
    z = (points[a][2] + points[b][2] + points[c][2]) / 3 # calculate average height of triangle
    for color in colors:
        if z <= color:
            return colors[color]
            break
        

class noise:

    def __init__(self, x, y):
        x, y = math.ceil(x) + 1, math.ceil(y) + 1
        self.gradients = []
        for j in range(y):
            self.gradients.append([])
            for i in range(x):
                a = random.uniform(0, 1)
                b = math.sqrt(1 - a ** 2)
                c = [-1, 1][random.randint(0,1)]
                d = [-1, 1][random.randint(0,1)]
                self.gradients[j].append([a * c, b * d])

    # previous code

    def dotGridGradient(self, ix, iy, x, y):
        dx = x - ix
        dy = y - iy
        return dx * self.gradients[iy][ix][0] + dy * self.gradients[iy][ix][1]
    
    def lerp(self, a0, a1, w):
        return a0 + w * (a1 - a0)


def _diamondSquare(self, stepsize, scale):
        half = int(stepsize/2)
        # diamond part
        for y in range(half, self.dims+half, stepsize):
            for x in range(half, self.dims+half, stepsize):
                diamondStep(x,y,half, scale)

        # square part
        for y in range(0, self.dims, stepsize):
            for x in range(0, self.dims, stepsize):
                
def mRand():
    mag = random.random()
    sign = random.random()
    if sign >=0.5:
        return mag
    return mag * -1.0
    
def diamondStep(self, x, y, half, scale):
     self.cells[x, y] = ((self.cells[x-half, y-half] + self.cells[x+half, y-half] + self.cells[x-half, y+half]
                          + self.cells[x+half, y+half])/4.0) + (mRand()*scale)


def squareStep(self,x,y,half,scale):
    self.cells[x+half,y] = ((self.cells[x+half+half, y] +
                             self.cells[x+half-half, y] + self.cells[x+half, y+half] + self.cells[x+half, y-half])/4.0)+(mRand()*scale)
                self.cells[x,y+half] = ((self.cells[x+half, y+half] + self.cells[x-half, y+half]
                                         + self.cells[x, y+half+half] + self.cells[x, y+half-half])/4.0)+(mRand()*scale)


"""
    Given a straight line segment specified by a starting point and an endpoint
    in the form of [starting_point_x, starting_point_y] and [endpoint_x, endpoint_y],
    a roughness value > 0, an initial vertical displacement and a number of
    iterations > 0 applies the  midpoint algorithm to the specified segment and
    returns the obtained list of points in the form
    points = [[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
"""

# Iterative midpoint vertical displacement
def midpoint_displacement(start, end, roughness, vertical_displacement=None,
                          num_of_iterations=16):
    
    # Final number of points = (2^iterations)+1
    if vertical_displacement is None:
        # if no initial displacement is specified set displacement to:
        #  (y_start+y_end)/2
        vertical_displacement = (start[1]+end[1])/2
    # Data structure that stores the points is a list of lists where
    # each sublist represents a point and holds its x and y coordinates:
    # points=[[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
    #              |          |              |
    #           point 0    point 1        point n
    # The points list is always kept sorted from smallest to biggest x-value
    points = [start, end]
    iteration = 1
    while iteration <= num_of_iterations:
        points_tup = tuple(points)
        for i in range(len(points_tup)-1):
            # Calculate x and y midpoint coordinates:
            # [(x_i+x_(i+1))/2, (y_i+y_(i+1))/2]
            midpoint = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2,
                                [0, 1]))
            # Displace midpoint y-coordinate
            midpoint[1] += random.choice([-vertical_displacement,
                                          vertical_displacement])
            # Insert the displaced midpoint in the current list of points         
            bisect.insort(points, midpoint)
        vertical_displacement *= 2 ** (-roughness)
        # update number of iterations
        iteration += 1
    return points
#importing stuff


import PIL

from PIL import Image
#Open image using Image module
im = Image.open("images/cuba.jpg")
#Show actual Image
im.show()
#Show rotated Image
im = im.rotate(45)
im.show()

top = Tk()

C = Canvas(top, bg="blue", height=250, width=300)
filename = Image(file = "C:\\Users\\location\\imageName.png")
background_label = Label(top, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

C.pack()
top.mainloop
