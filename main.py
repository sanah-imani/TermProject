# other important functions
#Source: https://www.cs.cmu.edu/~112/notes/
#notes-data-and-operations.html#FloatingPointApprox
def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)


#letting the user draw lines

#modules

from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#function
def plotOnScreen(x,y):
    root = Tk()
    fig, ax = plt.subplots()
    ax.axis("off")
    plot.plot(x, y, color="blue", marker="x", linestyle="")
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().grid(row=0, column=0)
    

#functions class
class Function(object):
    functions = ['Trignometry', 'Conic Sections', 'Polynomials', 'Classic Geometry', 'Piecewise']
    def __init__(self, startCoords, endCoords, showCoords):
        self.startCoords = startCoords
        self.endCoords = endCoords
        self.showCoords = showCoords
        self.move = True
    def getFunctions(self):
        return self.functions
    def placeFunction(self):
        allCoordsX = self.getCoords(self.startCoords, self.endCoords)
        for (funcX, funcY) in allCoords:
            for (pointX,pointY) in groundCoords:
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

    
#trignometry
class sine(Function):
    def __init__(self, startCoords, endCoords, showCoords, A, B, C, transformation):
        super().__init__(self, startCoords, endCoords, showCoords)
        self.A = A
        self.B = B
        self.C = C
        self.transformation = transformation
    def getCoords(self):
        x = np.arrange(showCoords[0][0], showCoords[1][0],0.1)
        y = np.sin(x)
        allCoords = []
        for i in range(len(x)):
            allCoords.append(x[i],y[i])
        return allCoords
    def __repr__(self):
        return "Asin(Bx) + C"

class cos(Function):
    def __init__(self, startCoords, endCoords, showCoords, A, B, C, transformation):
        super().__init__(self, startCoords, endCoords, showCoords)
        self.A = A
        self.B = B
        self.C = C
        self.transformation = transformation
    def getCoords(self):
        x = np.arrange(showCoords[0][0], showCoords[1][0],0.1)
        y = np.sin(x)
        return y
    def __repr__(self):
        return "Acos(Bx) + C"
    def instructions(self):
        return "Please enter the values of A, B, and C"

#conic sections
class hyperbola(Function):
    pass

#splash screen

class MyApp(App):
    def appStarted(self):
        path = ''
        self.image1 = self.loadImage(path)
        width,height = self.image1.size
        scaleFactor = 400/width
        self.image1 = self.scaleImage(self.image1, scaleFactor)
        

        #exiting a screen flag
        self.exit = False
        #modes
        self.keyPress1 = False #splashscreen Mode
        self.keyPress2 = False #help/instructions Mode
        self.keyPress3 = False #level chooser


        #important variables
        self.buttonsDim = [[100, 50]]
        self.levels = [False]*9
        

    def redrawAll(self, canvas):
        if self.keyPress1 == False:
            self.drawSplashScreen(canvas)
    
    def drawSplashScreen(self,canvas)
        canvas.create_image(self.width/2, self.height/2,
                            image=ImageTk.PhotoImage(self.image1))
        self.createButton(200, 300, self.buttonDim[0][0], self.buttonDim[0][1], "Play Now!", 'Arial 30 bold', 'white', 'red')


    def drawLevels(self,canvas):
        for row in range(3):
            for col in range(3):
                self.createButton(50*col + self.margin , 50*row + self.margin, self.buttonDim[0][0],
                                  self.buttonDim[0][1], "Play Now!", 'Arial 30 bold', 'white', 'red')
                
    def mousePressed(self, event):
        if self.keyPress1 == False:
            val = self.checkButtonPressed(event, self.buttonDim[0][0], self.buttonDim[0][1])
            if val:
                self.keyPress1 = True
                self.exit = True
        cx, cy = app.width/2, app.height/2

    def checkButtonPressed(self,event, height, width):
        if ((cx- (width/2) <= event.x <= cx+(width/2))
            and (cy-(height/2) <= event.y <= cy+(height/2))):
            return True
        return False
    def timerFired(self):
        if self.keyPress1 ==True:
            self.animateTransition(0, self.image1)
    def animateTransition(animateType, obj):
        if animateType == 0 and self.exit = True:
            obj = self.scaleImage(obj, .5)
            if obj.size == (X,Y):
                self.exit = False

    def createButton(self, cx, cy,height,width text, font, txtC, buttonC):
        canvas.create_rectangle(cx-(width/2), cy-(height/2), cx+(width/2), cy+(width/2), fill=buttonC)
        canvas.create_text(cx, cy, text= text, color=txtC, font = font)
    

#final terrain generation algorithm

import random
import math
import numpy as np



def diamond_square(shape: (int, int),
                   min_height: [float or int],
                   max_height: [float or int],
                   roughness: [float or int],
                   random_seed=None,
                   as_ndarray: bool = True):
    """Runs a diamond square algorithm and returns an array (or list) with the landscape
        An important difference (possibly) between this, and other implementations of the 
    diamond square algorithm is how I use the roughness parameter. For each "perturbation"
    I pull a random number from a uniform distribution between min_height and max_height.
    I then take the weighted average between that value, and the average value of the 
    "neighbors", whether those be in the diamond or in the square step, as normal. The 
    weights used for the weighted sum are (roughness) and (1-roughness) for the random
    number and the average, respectively, where roughness is a float that always falls 
    between 0 and 1.
        The roughness value used in each iteration is based on the roughness parameter
    passed in, and is computed as follows:
        this_iteration_roughness = roughness**iteration_number
    where the first iteration has iteration_number = 0. The first roughness value 
    actually used (in the very first diamond and square step) is roughness**0 = 1. Thus,
    the values for those first diamond and square step entries will be entirely random.
    This effectively means that I am seeding with A 3x3 grid of random values, rather 
    than with just the four corners.
        As the process continues, the weight placed on the random number draw falls from
    the original value of 1, to roughness**1, to roughness**2, and so on, ultimately 
    approaching 0. This means that the values of new cells will slowly shift from being
    purely random, to pure averages.
    OTHER NOTES:
    Internally, all heights are between 0 and 1, and are rescaled at the end.
    PARAMETERS
    ----------
    :param shape
        tuple of ints, (int, int): the shape of the resulting landscape
    :param min_height
        Int or Float: The minimum height allowed on the landscape
    :param max_height
        Int or Float: The maximum height allowed on the landscape
    :param roughness
        Float with value between 0 and 1, reflecting how bumpy the landscape should be.
        Values near 1 will result in landscapes that are extremely rough, and have almost no
        cell-to-cell smoothness. Values near zero will result in landscapes that are almost
        perfectly smooth.
        Values above 1.0 will be interpreted as 1.0
        Values below 0.0 will be interpreted as 0.0
    :param random_seed
        Any value. Defaults to None. If a value is given, the algorithm will use it to seed the random
        number generator, ensuring replicability.
    :param as_ndarray
        Bool: whether the landscape should be returned as a numpy array. If set
        to False, the method will return list of lists.
    :returns [list] or nd_array
    """

    # sanitize inputs
    if roughness > 1:
        roughness = 1.0
    if roughness < 0:
        roughness = 0.0

    working_shape, iterations = _get_working_shape_and_iterations(shape)

    # create the array
    diamond_square_array = np.full(working_shape, -1, dtype='float')

    # seed the random number generator
    random.seed(random_seed)

    # seed the corners
    diamond_square_array[0, 0] = random.uniform(0, 1)
    diamond_square_array[working_shape[0] - 1, 0] = random.uniform(0, 1)
    diamond_square_array[0, working_shape[1]-1] = random.uniform(0, 1)
    diamond_square_array[working_shape[0]-1, working_shape[1]-1] = random.uniform(0, 1)

    # do the algorithm
    for i in range(iterations):
        r = math.pow(roughness, i)

        step_size = math.floor((working_shape[0]-1) / math.pow(2, i))

        _diamond_step(diamond_square_array, step_size, r)
        _square_step(diamond_square_array, step_size, r)

    # rescale the array to fit the min and max heights specified
    diamond_square_array = min_height + (diamond_square_array * (max_height - min_height))

    # trim array, if needed
    final_array = diamond_square_array[:shape[0], :shape[1]]

    if as_ndarray:
        return final_array
    else:
        return final_array.tolist()


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


def _diamond_step(DS_array, step_size, roughness):
    """Does the diamond step for a given iteration.
    During the diamond step, the diagonally adjacent cells are filled:
    Value   None   Value   None   Value  ...
    None   FILLING  None  FILLING  None  ...
 
    Value   None   Value   None   Value  ...
    ...     ...     ...     ...    ...   ...
    So we'll step with increment step_size over BOTH axes
    """
    # calculate where all the diamond corners are (the ones we'll be filling)
    half_step = math.floor(step_size/2)
    x_steps = range(half_step, DS_array.shape[0], step_size)
    y_steps = x_steps[:]

    for i in x_steps:
        for j in y_steps:
            if DS_array[i,j] == -1.0:
                DS_array[i,j] = _diamond_displace(DS_array, i, j, half_step, roughness)


def _square_step(DS_array, step_size, roughness):
    """Does the square step for a given iteration.
    During the diamond step, the diagonally adjacent cells are filled:
     Value    FILLING    Value    FILLING   Value   ...
    FILLING   DIAMOND   FILLING   DIAMOND  FILLING  ...
 
     Value    FILLING    Value    FILLING   Value   ...
      ...       ...       ...       ...      ...    ...
    So we'll step with increment step_size over BOTH axes
    """

    # doing this in two steps: the first, where the every other column is skipped
    # and the second, where every other row is skipped. For each, iterations along
    # the half-steps go vertically or horizontally, respectively.

    # set the half-step for the calls to square_displace
    half_step = math.floor(step_size/2)

    # vertical step
    steps_x_vert = range(half_step, DS_array.shape[0], step_size)
    steps_y_vert = range(0, DS_array.shape[1], step_size)

    # horizontal step
    steps_x_horiz = range(0, DS_array.shape[0],   step_size)
    steps_y_horiz = range(half_step, DS_array.shape[1],   step_size)

    for i in steps_x_horiz:
        for j in steps_y_horiz:
            DS_array[i,j] = _square_displace(DS_array, i, j, half_step, roughness)

    for i in steps_x_vert:
        for j in steps_y_vert:
            DS_array[i,j] = _square_displace(DS_array, i, j, half_step, roughness)


def _diamond_displace(DS_array, i, j, half_step, roughness):
    """
    defines the midpoint displacement for the diamond step
    :param DS_array:
    :param i:
    :param j:
    :param half_step:
    :param roughness:
    :return:
    """
    ul = DS_array[i-half_step, j-half_step]
    ur = DS_array[i-half_step, j+half_step]
    ll = DS_array[i+half_step, j-half_step]
    lr = DS_array[i+half_step, j+half_step]

    ave = (ul + ur + ll + lr)/4.0

    rand_val = random.uniform(0,1)

    return (roughness * rand_val) + (1.0 -roughness) * ave


def _square_displace(DS_array, i, j, half_step, roughness):
    """
    Defines the midpoint displacement for the square step
    :param DS_array:
    :param i:
    :param j:
    :param half_step:
    :param roughness:
    :return:
    """
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



















import tkinter as tk
from time import sleep

def getpoint1(event):
    global x, y
    x, y = event.x, event.y

def getpoint2(event):
    global x1, y1
    x1, y1 = event.x, event.y

def drawline(event):
    canvas.create_line(x, y, x1, y1)



root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

root.bind('q', getpoint1)
root.bind('w', getpoint2)
root.bind('<Button-1>', drawline)


root.mainloop()

#adding a button
button1 = tk.Button (root, text=' Create Charts ',command=create_charts, bg='palegreen2', font=('Arial', 11, 'bold')) 
canvas1.create_window(400, 180, window=button1)

#adding a label

label1 = tk.Label(root, text='Graphical User Interface')
label1.config(font=('Arial', 20))
canvas1.create_window(400, 50, window=label1)

entry1 = tk.Entry (root)
canvas1.create_window(400, 100, window=entry1) 
  
entry2 = tk.Entry (root)
canvas1.create_window(400, 120, window=entry2) 
          
entry3 = tk.Entry (root)
canvas1.create_window(400, 140, window=entry3)

#screen recording feature
#necessary installations - pip3 install numpy opencv-python pyautogui
## display screen resolution, get it from your OS settings
SCREEN_SIZE = (1920, 1080)
# define the codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# create the video write object
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (SCREEN_SIZE))

while True:
    # make a screenshot
    img = pyautogui.screenshot()
    # convert these pixels to a proper numpy array to work with OpenCV
    frame = np.array(img)
    # convert colors from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # write the frame
    out.write(frame)
    # show the frame
    cv2.imshow("screenshot", frame)
    # if the user clicks q, it exits
    if cv2.waitKey(1) == ord("q"):
        break

# make sure everything is closed when exited
cv2.destroyAllWindows()
out.release()
#getting the screenshot
img = pyautogui.screenshot(region=(0, 0, 300, 400))


#pagination and frames
#Source: https://www.youtube.com/watch?v=Zw6M-BnAPP0
class mathChallenge(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.root = tk.Tk()
        tk.Tk.__init__(self, *args, **kawrgs)
        tk.Tk.iconbitmap(self, default="client.ico")
        tk.Tk.wm_title(self, "Math Challenge")
        container = tk.Frame(self)
        container.pack(side="top",fill="both", expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.frames = {}

        frame = Homepage(container,self)
        self.frames[Homepage] = frame
        frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(StartPage)

        def show_frame(self,count):
            frame = self.frames[count]
            frame.tkraise()


class Homepage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Welcome to XXX", font=MY_FONT)
        label.pack(pady=20,padx=20)
        desc = tk.Label(self, text="Lorem ipsum ....", font=MY_FONT2)
        desc.pack(pady=20,padx=20)
        button = ttk.Button(self, text="Help",
                            command=lambda: controller.show_frame(HelpP))
        button.pack()
     
        button2 = ttk.Button(self,text="Test out functions",
                             command=lambda: controller.show_frame(TestP))
        button2.pack()
        button3 = ttk.Button(self, text="Start Game"
                             command=lambda: controller.show_frame(StartGame))
        button3.pack()
        
class HelpP(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Want to know how to Play?", font=My_FONT)
        label.pack(pady=20,padx=20)

class levelChooser(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Choose your level", font=MY_FONT)
        label.pack(pady=20,padx=20)
        root = Tk()
        frame=Frame(root)
        Grid.rowconfigure(root, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)
        frame.grid(row=0, column=0, sticky='nsew')
        grid=Frame(frame)
        grid.grid(sticky='nsew', column=0, row=7, columnspan=2)
        Grid.rowconfigure(frame, 7, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        
        levels = [i for i in range(1,20)]
        #example values
        for x in range(5):
            for y in range(5):
                if (self.levels[i]):
                    btn = Button(frame, text=f'{levels[i]}')
                    btn.grid(column=x, row=y, sticky='nsew')

        for x in range(10):
          Grid.columnconfigure(frame, x, weight=1)

        for y in range(5):
          Grid.rowconfigure(frame, y, weight=1)


class functionEditor(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Edit your function", font=MY_FONT)
        label.pack(pady=20,padx=20)
        root = Tk()
        frame=Frame(root)
        label = tk.Label(self, text="Choose", font=MY_FONT)
        
        
        
        
        
#embedding a background video
import imageio
from tkinter import Tk, Label
from PIL import ImageTk, Image
from pathlib import Path

video_name = str(Path().absolute()) + '/../background.mp4'
video = imageio.get_reader(video_name)
delay = int(1000 / video.get_meta_data()['fps'])
      
def stream(label):
  
  try:
    image = video.get_next_data()
  except:
    video.close()
    return
  label.after(delay, lambda: stream(label))
  frame_image = ImageTk.PhotoImage(Image.fromarray(image))
  label.config(image=frame_image)
  label.image = frame_image

#animating and setting up the character
WIDTH = 800
HEIGHT = 500

tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="light blue")
tk.title("Jump Around")
canvas.pack()

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
                         
        self.image = canvas.create_image(WIDTH / 2, HEIGHT-100, anchor=NW,
                                         image=self.frames_l[0])
        self.speedx = 0
        self.speedy = 0
        canvas.bind_all("<KeyPress-Left>", self.move)
        canvas.bind_all("<KeyPress-Right>", self.move)
        canvas.bind_all("<KeyPress-space>", self.jump)
        canvas.bind_all("<KeyRelease-Left>", self.stop)
        canvas.bind_all("<KeyRelease-Right>", self.stop)
        self.jumping = False
        self.current_frame = 0
        self.last_time = time.time()

def animate(self):
        now = time.time()
        if now - self.last_time > 0.05:
            self.last_time = now
            self.current_frame = (self.current_frame + 1) % 4
        if self.speedx < 0:
            canvas.itemconfig(self.image, image=self.frames_l[self.current_frame])
        if self.speedx > 0:
            canvas.itemconfig(self.image, image=self.frames_r[self.current_frame])
class Mode:
    def __init__(self):
        self.assistenceMode = False
        self.normalMode = True
        self.tutorialMode = True
        self.selectMode = False

#tutorial pop-up
def do_popup(self, event):
    self.popup_menu.post(event.x_root, event.y_root)

#quiting
b = Button(root, text="Quit", command=root.destroy)
b.pack()
#when you set up 
self.bind("<Button-3>", self.do_popup)

#tutorial image
from PIL import ImageTk,Image
imageName = ""
image = ImageTk.PhotoImage(Image.open(imageName))
canvas.create_image(20, 20, anchor=NW, image=img)

#creating our navigation bar
#http://effbot.org/tkinterbook/menu.htm
menubar = Menu(root)
editMenu = Menu(menubar, tearoff=0)
editMenu.add_command(label="Add a Path", command="addP")
editMenu.add_command(label="Delete a Path",command="deleteP")
editMenu.add_separator()
editMenu.add_command(label="Path Hints",command="hintsP")
menubar.add_cascade(label="Edit Path", menu=editMenu)
menubar.add_cascade(label="De", menu=editmenu)


def keyPressed(app,event):
    if (event.key == "s"):
        self.selectMode = True
    if (event.key == "r"):
        self.gameStart()


#functions adder
import requests
from bs4 import BeautifulSoup

functionsDropDown = []
lb=Listbox(window, height=5, selectmode='multiple')
for val in data:
    lb.insert(END,val)
lb.place(x=250, y=150)
mylistbox.bind('<<ListboxSelect>>',CurSelect)
#function entry 
self.functionEntry=tk.Entry(self.bottomChatFrame)
self.addFunction=tk.Button(self.bottomChatFrame, text="Send", command=self.sendChatData(self.chatEntry.get(), "Professor", self.timePassed))
self.functionEntry.pack(side=TOP, fill=BOTH)
self.addFunction.pack(side=BOTTOM, fill=BOTH,ipady=5)
self.sendChatEntry.pack(side=BOTTOM, fill=BOTH,ipady=5)

def CurSelect(evt):
    self.function = str(lb.get(mylistbox.curselection()))
    
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


def mousePressed(self,event):
    if (self.selectMode):
        self.selectCoords.append((event.x,event.y))
        if len(self.selectCoords) == 2:
            self.plotFunction(self.selectCoords[0], self.selectCoords[1])
            self.selectCoords = []
    
def plotFunction(self, xy1, xy2):
    

app = mathChallenge()
