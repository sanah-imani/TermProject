Project Description 


Title: Addventure


An interactive game that requires users to use their math skills to navigate through terrains. A linear function to complete a break? A piecewise function to create a “bridge”? Using parabolas to help collect a star? Complete your path using a range of functions, keep in line with physics, and run your avatar to maximise your reward toward your target. This version consists of 5 levels where you need to move your avatar from the entrance to the target but need to fix the breaks and collect awards using functions.


How to run the project:


1. If using a Mac: run removeFiles.py first 
2. Then simply run the gameClass_main.py file: You will have to navigate through the Canvas Window (Instructions placed below).
3. Ensure that the images are in the same folder as gameClass_main.py.
4. Other files (automatically imported in gameClass_main.py): character.py, terrain.py, functions.py, cmu_112_graphics.py.
5. Ensure that the images and image folders are as is.


Libraries:


No specific library to be externally installed, but there are the import:


from cmu_112_graphics import *
import os
import time
import random
import bisect
import math
import csv


Shortcut commands:


* Lowercase letter p - switches to a higher level automatically
* Lower “q” - skips to the end of the level
* Lower “w” - you win the level automatically

Full Instructions


Overall Goal: The objective of the game is to bridge the gaps between the terrains to reach the targets and complete the levels using functions. The functions are plotted on the tkinter canvas with respect to its coordinate system.


Detailed Instructions on running the game:


1) Navigate to the levels menu by clicking on the play button and choose the appropriate level


2) Your avatar will be placed at the entrance bar and you can press the "Right" arrow to move. The avatar can move to the right only.


3) To bridge the gap first choose the start and end points of the function by pressing the 's' key. then click on the terrain points and blue bars will appear to show the region selection.


4) Choose the function from the menu (if the text in the menu disappears you have run out of stock of that function!). To add a function select the plus button at the top game bar.


5) Add all the parameters values by clicking on the text "change value of ..". Click add function and press the down array to move function. Remember to settle the position of this function before you add another function.