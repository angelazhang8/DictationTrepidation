from tkinter import *
from math import *
from time import *
from random import *
import itertools

root = Tk()
screen = Canvas(root, width=600, height=600, background="white")

def setInitialValues():
    global x1, y1, x2, y2, mouseDown, line, xPrev, yPrev, writeFile
    
    mouseDown = False
    xPrev = 0
    yPrev = 0

    writeFile = open("out.txt", "w")


#GETS CALLED WHENEVER THE MOUSE IS CLICKED DOWN
def mouseClickHandler( event ):
    global mouseDown,x1, y1
    
    mouseDown = True
    x1 = event.x
    y1 = event.y


#GETS CALLED WHENEVER THE MOUSE IS CLICKED DOWN
def mouseMotionHandler( event ):
    global x2, y2, line, xPrev, yPrev

    x2 = event.x
    y2 = event.y
    if mouseDown == True:
        #screen.delete(line)
        line = screen.create_line(x2,y2, xPrev, yPrev, fill="red", width = 2)
    xPrev = x2
    yPrev = y2

#GETS CALLED WHENEVER THE MOUSE IS RELEASED
def mouseReleaseHandler( event ):
    global mouseDown, line

    mouseDown = False

    #This is needed to make the final line stay on screen and
    #not get deleted when the user starts the next line
#    line = screen.create_line(x1,y1, x2, y2, fill="red")

def theFalling():
def keyDownHandler( event ):
    if event.keysym == "KP_Enter":   
    
#CALLS THE PROCEDURE setInitialValues 0 MILLISECONDS AFTER STARTING THE PROGRAM
root.after(0, setInitialValues)

#BINDS THE PROCEDURE mouseClickHandler TO ALL MOUSE-DOWN EVENTS
screen.bind("<Button-1>", mouseClickHandler)

#BINDS THE PROCEDURE mouseReleaseHandler TO ALL MOUSE-UP EVENTS
screen.bind("<Motion>", mouseMotionHandler)

#BINDS THE PROCEDURE mouseReleaseHandler TO ALL MOUSE-UP EVENTS
screen.bind("<ButtonRelease-1>", mouseReleaseHandler)

screen.bind ( "<Key>", keyDownHandler )
screen.pack()
screen.focus_set()
root.mainloop()
