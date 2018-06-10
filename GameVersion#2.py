from tkinter import *
from math import *  #only if you need sqrt, pi, sin or cos
from time import *
from random import *
import itertools

root = Tk()
root.title("somethingelse")
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.attributes('-fullscreen', True)
s = Canvas(root, width=sw, height=sh, highlightthickness=0, bg="white")
s.pack()

##s = Canvas(root, width=1200, height=900, background="white")


            
def setInitialValues():
    global teacher, XX, YY, x1, y1, x2, y2, writeFile, file
    global teacherGIF, line, xPrev, yPrev, myText, aY, aX, strokes, char
    global mouseDown, startTime 
    teacherGIF = PhotoImage(file = "asianFather.gif")
    insults = ["You got stung by a bee? Next time get stung by an A",
               "You’re 5 years old? When I was your age I was 6",
               "After you are done studying you can go play...piano for 5 hours",
               "Do barrel roll? How about get honour roll",
               "Homework finished? DO IT AGAIN",
               "You got 99 problems? You solve each one",
               "Onry 96% on maths test? DISOWNED",
               "Calculus why not calcuMORE?",
               "What is Aisan without A’s? SIN",
               "Every day you shuffling? How about everyday you studying?",
               "Less Facebook, more face in book",
               "If at first you don’t succeed, don’t come back home",
               "You forget to study, I forget to feed you",
               "Calculator? Why not calcunow?",
               "You got 99%? I put this on the refrigerator...OF SHAME",
               "Your mother gave birth to you in C-section. You disappoint me from the start",
               "You can go to any school you like. As long as it is medical school",
               "Like a boss? Why not the boss?",
               "Extra credit? You mean bonus fun",
               "Smashing pumpkins? At your age you should be smashing atoms",
               "You can program in C++? Why not A++",
               "Doctor Who? Why not doctor you?"]
    XX = []
    YY = []
    aX = []
    aY = []
    
    strokes = []
    char = []
    
    startTime = 0

    xPrev = 0
    yPrev = 0
    myText = 0
    mouseDown = False
    writeFile = open("out.txt", "w")

def end(event):
    root.destroy()
    exit()
    
def drawObjects(everySoOften):
    global teacher, teacherGIF, teacherSIZED, myText, file
    teacherSIZED = teacherGIF.zoom(2)
    teacher = s.create_image(sw/2, sh/2, image = teacherSIZED)
    if timeElapsed%10 == 0:
        s.delete(myText)
        file = open("chineseCHAR.txt", encoding="utf8")
        line = choice(file.readlines()).replace("\n", "")
        myText = s.create_text(sw/2, sh/5, text = line, font = "Helvetica 20", fill = "blue")

def everySoOften( ):
    global gameClock, timeElapsed
    timeElapsed = int(time() - startTime)

def deleteStrokes():
    global char
    for i in range(len(XX)):
        for f in range(len(XX[i])):                          
            s.delete(char[i][f])
            
##def createStrokes():
##    global strokes, speed
   
                
def afterPressingEnter ( event ):
    global XX, YY, speed
    speed = 0
    s.create_rectangle(0, 0, sw, sh, fill = "white")

    #Assigning 0 values
    for x in range(len(XX)):
        for y in range(len(XX[x])):           
            strokes.append(0)
        char.append(strokes)
       
    #Remaking the lines
    for x in range(100):
        for i in range(len(XX)):
            for f in range(len(XX[i])-1):
                strokes[f] = s.create_line(XX[i][f], YY[i][f] + speed , XX[i][f + 1], YY[i][f + 1] +speed, fill = "black")

        speed += 5
        s.update()
        sleep(0.03)
        deleteStrokes()
        
        
    XX = []
    YY = []
    
def recursive_len(item):
    if type(item) == list:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1        
    
def mouseClickHandler( event ):
    global mouseDown,x1, y1, aX, aY
    
    mouseDown = True

    x1 = event.x
    y1 = event.y    


#def updateObjects():
def mouseMotionHandler( event ):
    global x2, y2, line, xPrev, yPrev, x1, y1, writeFile
    global mouseDown, aX, aY
    x2 = event.x
    y2 = event.y
    
    if mouseDown == True:
        line = s.create_line(x2,y2, xPrev, yPrev, fill="black", width = 2)
        aX.append(x2)
        aY.append(y2)
        

##    writeFile.write(x2)
##    writeFile.write(y2)
    
    xPrev = x2
    yPrev = y2

def mouseReleaseHandler( event ):
    global mouseDown, line, XX, YY, aX, aY

    mouseDown = False
    XX.append(aX)
    YY.append(aY)
    
    aX = []
    aY = []
    
def keyDownHandler( event ):
    if event.keysym == "w":
        s.create_rectangle(0, 0, sw, sh, fill = "white")
        #print (XX)
        print (len(XX))          
    
#def keyUpHandler( event ):

def runGame():
    setInitialValues()
    
    while True:  
        
        everySoOften()
        #drawObjects(everySoOften)
        s.update()
             
        #s.delete(  )
        #updateObjects()
        #checkForCollisions()

    endGame()

#At the bottom

root.after( 500, runGame )

s.bind( "<Button-1>", mouseClickHandler )

s.bind ( "<Key>", keyDownHandler )

#s.bind( "<KeyRelease>", keyUpHandler )

s.bind("<Motion>", mouseMotionHandler)

s.bind("<ButtonRelease-1>", mouseReleaseHandler)

s.configure(cursor="crosshair")

s.bind("<Escape>", end)

s.bind("<Return>", afterPressingEnter)

s.focus_set()

s.pack()
s.focus_set()
root.mainloop()
