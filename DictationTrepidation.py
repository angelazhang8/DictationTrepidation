import time
import itertools
import linecache
import tkinter as tk
from random import *
from tkinter import simpledialog, messagebox

#Link to design document
#https://docs.google.com/document/d/1A_xqdYQaaSnKIntLaIf4LAuNlfgdjtp1BI297VQle8E/edit?usp=sharing

#--------------------------------------------------------------------------
# For making the falling characters
#--------------------------------------------------------------------------
class ChineseCharacter:     #After pressing arrow keys/clicking prev or next, characters fall down

    def __init__( self , s ):
        self.mouseDown = False
        self.s = s
        self.aX = []    #To be filled with strokes (every continuous drawing made)
        self.aY = []
        self.XX = []    #To be filled with characters (a collection of strokes)
        self.YY = []
        self.char = []
    
    def mouseMotionHandler( self, event ):
        x = event.x
        y = event.y
        if self.mouseDown == True:
            
            if len(self.aX) != 0:
                seg = self.s.create_line(x , y, self.aX[-1], self.aY[-1], fill="black", width = 2)  #Create the many lines so that the user can "draw"
                self.char.append(seg)
                
            self.aX.append(x)
            self.aY.append(y)

    def mouseReleaseHandler ( self, event ):
        self.mouseDown = False
        self.XX.append(self.aX)
        self.YY.append(self.aY)
        self.aX = []
        self.aY = []

    def mouseClickHandler(self, event):
        self.mouseDown = True

    def fallingCharacters ( self ):
        speed = 0
        #Animating falling action
        for x in range(70):
            
            for seg in self.char: #Deleting the characters
                self.s.delete(seg)
                
            self.char = []

            #Remaking the lines so that they're strokes within each character
            for i in range(len(self.XX)):
                aX = self.XX[i]
                aY = self.YY[i]
                
                for f in range(len(aX)-1):
                    seg = self.s.create_line(aX[f] , aY[f] + speed, aX[f + 1], aY[f + 1] + speed, fill="black", width = 2)
                    self.char.append(seg)

            speed += 7
            s.update()
            time.sleep(0.03)

        for seg in self.char:
            self.s.delete(seg)

        #Clean out arrays for the next drawing
        self.aX = []
        self.aY = []
        self.XX = []
        self.YY = []
        self.char = []

#--------------------------------------------------------------------------
# For displaying characters
#--------------------------------------------------------------------------
class DisplayedCharacter:

    def __init__(self, posx, posy, level, filename):
        global wrongAnswers, total
        
        wrongAnswers = 0
        
        self.testMode = False   #practice mode
        self.posx = posx 
        self.posy = posy
        self.index = 0
        self.groupIndex = 0
        
        if level == 0:          # "easy"
            self.num = 3
            self.wa = 10
            
        elif level == 1:        # "medium"
            self.num = 6
            self.wa = 5
            
        elif level == 2:        # "hard"
            self.num = 10
            self.wa = 3
            
        else:                   # "extreme"
            self.num = 25
            self.wa = 1
            
        self.chars = []         # (pinyin, cchar, definition)
        
        self.readFromFile(filename)
        
        self.text1 = None
        self.text2 = None
        self.text3 = None
        self.answer = None
        total = None
                      
    def readFromFile(self, filename):
        myfile = open("ChineseCHAR.txt", "r", encoding="utf-8")
        lines = myfile.readlines()
      
        for line in lines:
            cchar = line.split(",", 1)[0].split(".", 1)[1]     #Get chinese character from file
            
            pinyin = (line.split("(", 1)[1]).split(")")[0]      #Get pinyin from file
         
            definition = (line.split("-", 1)[1])    #Get english translation from file
        
            length = len(definition.split(",")[:])        #Lists top three definitions for each character
            
            if length < 3:
                pass
            
            else:
                definition = definition.split(",")[0] + ", " + definition.split(",")[1] + ", " + definition.split(",")[2]

            self.chars.append((pinyin, cchar, definition))
            
    def nextGroup(self):
        testMode = False
        self.index += self.num
        
        if self.index >= len(self.chars):
            self.index = 0
            
        self.groupIndex = 0

    def takeTest(self):
        self.testMode = True
        self.groupIndex = 0
        
    def makeChineseChars(self, s, forward):
        global total
        
        print("testMode=" + str(self.testMode) + ", groupIndex=" + str(self.groupIndex))
        
        if self.text1 != None:
            s.delete(self.text1)
            
        if self.text2 != None:
            s.delete(self.text2)
            
        if self.text3 != None:
            s.delete(self.text3)

        pinyin, cchar, definition = self.chars[self.index + self.groupIndex]
        self.text1 = s.create_text(self.posx, self.posy - 75, text = pinyin, font = "Helvetica 30", fill = "red")
        
        if self.testMode == False:
            self.text2 = s.create_text(self.posx, self.posy, text = cchar, font = "Helvetica 85", fill = "blue")
            
        else:
            self.answer = (pinyin, cchar, definition)
            
        self.text3 = s.create_text(self.posx, self.posy + 75, text = definition, font = "Helvetica 30", fill = "red")

        if forward == True:
            self.groupIndex += 1        # next
            
        else:
            self.groupIndex -= 1        # prev

        if self.groupIndex < 0:
            self.groupIndex = self.num - 1
            
        if self.groupIndex == self.num:
            self.groupIndex = 0
            
            if self.testMode == True:
                self.testMode = False       
                return True             # move to next group
            
        total = self.index
        return False                    # stay in this group
        
    def showAnswer(self, s):
        global wrongAnswers, newWord
        pinyin, cchar, definition = self.answer
        
        if newWord == False:
            return
        
        newWord = False
        wrongAnswers += 1

        if wrongAnswers > self.wa:
            messagebox.showinfo(parent=root, title="Too bad too sad\n", message="Looks like you failed the course\n" + choice(insults))
            failingCourse2()
            
        if self.text2 != None:
            s.delete(self.text2)
            
        self.text2 = s.create_text(self.posx, self.posy, text = cchar, font = "Helvetica 85", fill = "blue")                   

#--------------------------------------------------------------------------
# Setting up canvas backgroud: image, tian zi box, clock, buttons
#--------------------------------------------------------------------------
def drawBackground():
    global s, sw, sh, bamboo
    
    bamboo = tk.PhotoImage(file = "bamboo.gif")
    s.create_image(sw/2, sh/2, image = bamboo)
    
    drawTianzi(s, sw, sh)
    drawClock(s, sw, sh)
    drawButtons(s, sw, sh)

def drawTianzi(s, sw, sh):
    '''Draw 2 tian zi boxes'''
    xcenter = sw/2
    ycenter = sh/2
    #Box 1
    s.create_rectangle(xcenter - 400, ycenter - 200, xcenter , ycenter + 200, fill = "#fffdf2")
    s.create_line(xcenter - 400, ycenter - 200, xcenter , ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter , ycenter - 200, xcenter - 400, ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter , ycenter - 200, xcenter - 400, ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter , ycenter - 200, xcenter - 400, ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter - 200, ycenter - 200, xcenter - 200, ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter , ycenter, xcenter - 400, ycenter, dash = (5, 2), fill = "grey")
    #Box 2
    s.create_rectangle(xcenter , ycenter - 200, xcenter + 400, ycenter + 200, fill = "#fffdf2")
    s.create_line(xcenter , ycenter - 200, xcenter + 400, ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter + 400, ycenter - 200, xcenter , ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter + 400, ycenter - 200, xcenter , ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter + 400, ycenter - 200, xcenter , ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter + 200, ycenter - 200, xcenter + 200, ycenter + 200, dash = (5, 2), fill = "grey")
    s.create_line(xcenter + 400, ycenter, xcenter , ycenter, dash = (5, 2), fill = "grey")

def drawClock(s, sw, sh):
    '''Draw empty clock. Its will be redraw to show stats.'''
    global clockDisplay
    clockDisplay = s.create_text(sw/2, sh*4/5 - 50, text = "clock", font = "Skia 30", fill = "white")

def drawButtons(s, sw, sh):
    '''Draw 3 buttons'''
    global prevButton, nextButton, actionButton
    
    prevButton = tk.Button(s, text="Prev", font = "Skia 20" , width=100, height=30, activebackground = "#33B5E5", borderwidth = 5, relief = tk.SUNKEN)
    prevButtonWin = s.create_window(sw-500, sh-200, anchor=tk.NW, width=100, height=30, window=prevButton)
    
    nextButton = tk.Button(s, text = "Next", width=80, font = "Skia 20" ,height=30, activebackground = "#33B5E5", borderwidth = 5, relief = tk.SUNKEN)
    nextButtonWin = s.create_window(sw-350, sh-200, anchor=tk.NW, width=100, height=30, window=nextButton)
    
    actionButton = tk.Button(s, text = "Take Test", font = "Skia 20" ,width=80, height=30, activebackground = "#33B5E5", borderwidth = 5, relief = tk.SUNKEN)
    actionButtonWin = s.create_window(sw-200, sh-200, anchor=tk.NW, width=100, height=30, window=actionButton)

#--------------------------------------------------------------------------
# Run game
#--------------------------------------------------------------------------
def updateClock():
    '''Update every 1000 ms to show stats'''
    global root, clockDisplay, elapsed, practiced, wrongAnswers
    #Game information at bottom of the screen
    msg = "Elapsed: " + str(elapsed) + "    Practiced " + str(practiced) + "    Wrong answers: " + str(wrongAnswers)
    
    elapsed += 1 # Every time this function is called, this gets updated
    s.delete(clockDisplay)
    clockDisplay = s.create_text(sw/2, sh*4/5 - 50, text = msg, font = "Skia 35 bold", fill = "white") #Text for the clock
    root.after(1000, updateClock)
    
def prevQuestion( event ) : 
    '''Show prev question. Only move in practice mode. Bind Prev button and left arrao key.'''
    global ch, mv, practiced
    
    if testMode == True: #If the player is in test mode, this button is disabled
        return
    
    mv.makeChineseChars(s, False)   #The index gets subtracted by 1 when the parameter is False
    ch.fallingCharacters()
    practiced += 1  
    
def nextQuestion( event ) : 
    '''Show next question. Bind Next button and right arrow key.'''
    global ch, mv, testMode, actionButton, elapsed, practiced, root, nextGroup, insults, rightAnswers, red, newWord

    if testMode == True:
        newWord = True  #New word is used to determine if the wrongAnswers tally needs to increase (it doesn't increase if they've already pressed the button)
        
    if nextGroup == True: #Next dictation
        messagebox.showinfo(parent=root, title="Important message", message="New Dictation Group!\n" + choice(insults))
        
        mv.nextGroup()
        mv.makeChineseChars(s, True)
        
        testMode = False    #First the user practices before their next dictation
        nextGroup = False   #Can only be true once they finish their dictation
        actionButton.config (text = "Take test")
        
    if testMode == True:
        rightAnswers += 1
        
    nextGroup = mv.makeChineseChars(s, True)
    ch.fallingCharacters()
    
    elapsed = 0
    practiced += 1
    
def takeAction( event ) : 
    '''If in practice mode, switch to test mode. If in test mode, show answer. 
       Bind Action button, Enter key, and Up arrow key'''
    global testMode, s, mv, newWord

    if testMode == False:
        testMode = True     #Function only gets called when they are switching from practice to test
        newWord = True
        mv.takeTest()
        mv.makeChineseChars(s, True)
        actionButton.config(text="I forgot")     #reconfigure button for new purpose
        
    else:
        mv.showAnswer(s)
    
def endGame( event ):   #Quit the game completely
    global root
    root.destroy()
    quit()

def bindHandler() :     #Bottom of the screen bindings
    global s, ch, mv, prevButton, nextButton, actionButton
    
    s.bind("<Button-1>", ch.mouseClickHandler )
    s.bind("<ButtonRelease-1>", ch.mouseReleaseHandler)
    s.bind("<Motion>", ch.mouseMotionHandler)
   
    prevButton.bind("<ButtonRelease-1>", prevQuestion)
    s.bind("<Left>", prevQuestion)

    nextButton.bind("<ButtonRelease-1>", nextQuestion)
    s.bind("<Right>", nextQuestion)

    actionButton.bind("<ButtonRelease-1>", takeAction)
    s.bind("<Return>", takeAction)

    s.bind("<Up>", takeAction)

    s.bind("<Escape>", endGame)

    s.focus_set()

#--------------------------------------------------------------------------
#Initial Values
#--------------------------------------------------------------------------
def setInitialValues():
    global root, sw, sh, testMode, elapsed, practiced, nextGroup
    global s, mv, ch, bamboo, startGame, insults, rightAnswers
    global clockDisplay, prevButton, nextButton, actionButton, practiced
    global newWord

    testMode = False
    elapsed = 0
    practiced = 0
    newWord = False
    mv = None
    ch = None
    clockDisplay = None 
    prevButton = None
    nextButton = None
    actionButton = None
    nextGroup = False
    #Screen info
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.title("DictationTrepidation")
    s = tk.Canvas(root, width=sw, height=sh, highlightthickness=0, bg="black")
    s.pack()
    s.configure(cursor="pirate")
    #Images
    bamboo = tk.PhotoImage(file = "bamboo.gif")
    s.create_image(sw/2, sh/2, image = bamboo)
    
    rightAnswers = 0
    startGame = False
    
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
    
def runGame(level):
    global root, sw, sh, s, mv, ch

    ch = ChineseCharacter(s)
    mv = DisplayedCharacter(sw/2, sh/5, level, "ChineseCHAR.txt")
    drawBackground()
    mv.makeChineseChars(s, True)
    bindHandler()
    root.after(100, updateClock)
        
def promptForLevel():
    global root, startGame, level
    l = None
    while l == None :
        l = simpledialog.askinteger("Choose a level", 
                "choose a level: 0 easy, 1 intermediate, 2 hard, 3 extreme", 
                parent=root, initialvalue=0, minvalue=0, maxvalue=3)
        
    startGame = True
    level = l

def showInstruction():
    global root
    messagebox.showinfo(parent=root, title="Instruction", message=
            "You are a student in KW chinese school and you don't want to "
            "let down your chinese school teacher or your parents. In order "
            "to do this, you must pass all of your dictations for the course. "
            "You will be given a number of words given per dictation that is "
            "dependent upon the difficulty level you choose. You will have time "
            "to 'study' for dictations before being tested. Beware! If you fail "
            "more than three dictations, you're kicked out of the course. Good luck!")

    
def introScreen():
    global bamboo, level, startGame
    global root, sw, sh, s, mv, ch, w, h
    global a, b1, b2, b3, b4, b6, b7, level

    w = 200
    h = 50

    b1 = s.create_text(sw/2, sh/2 - 300, text = "Dictation Trepidation", font = "Skia 80 bold", fill = "black")
    b4 = s.create_text(sw/2 + 5, sh/2 - 297, text = "Dictation Trepidation", font = "Skia 80 bold", fill = "white")

    b2 = s.create_rectangle ( sw/2 - w, sh*2/5 - h, sw/2 + w, sh*2/5 + h, fill = "#423100", outline = "#ffdd77", width = 11)
    b3 = s.create_rectangle (sw/2 - w, sh*3/5 - h, sw/2 + w, sh*3/5 + h, fill = "#423100", outline = "#ffdd77", width = 11)

    b6 = s.create_text (sw/2, sh*2/5, text = "see instructions", font = "Skia 30", fill = "white")
    b7 = s.create_text (sw/2, sh*3/5, text = "play game", font = "Skia 30", fill = "white")
 
    s.bind("<Button-1>", clicked)
    s.bind("<Escape>", endGame)
    
    while startGame == False:

        s.update()
        
        time.sleep(0.03)

    s.delete(b2, b3, b6, b7, b1, b4)
    
def failingCourse2():
    global sw, sh, failingFrame, wrongAnswers, practiced, total, rightAnswers

    failingFrame = tk.Frame(root, width=sw, height=sh , bg = "black")
    tk.Label(failingFrame, image = bamboo).place(x=sw/2, y=sh/2 , anchor = tk.CENTER)
    
    tk.Label(failingFrame, text = "A valiant effort! However not quite there yet!", font = "Skia 40", fg = "white", bg = "black").place(x=sw/2, y=sh/2 - 200,  anchor = tk.CENTER)
    tk.Label(failingFrame, text = "You got " + str(wrongAnswers) + " out of " + str(rightAnswers + wrongAnswers) + " wrong! Good job!", font = "Skia 40", fg = "white", bg = "black").place(x=sw/2, y=sh/2 - 150, anchor = tk.CENTER)
    tk.Label(failingFrame, text = "Better luck next time", font = "Skia 40", fg = "white", bg = "black").place(x=sw/2, y=sh/2 - 100, anchor = tk.CENTER)
    
    playAgainButton = tk.Button(failingFrame, text = "play again", font = "Skia 20")
    playAgainButton.place(x=sw/2, y=sh/2 - 20, anchor = tk.CENTER)
    failingFrame.place(x=sw/2, y=sh/2, anchor = tk.CENTER)

    playAgainButton.bind("<ButtonRelease-1>", deleteFailingFrame)

def deleteFailingFrame( event):
    global failingFrame, root
    
 #   time.sleep(1)
    root.destroy()
    root = tk.Tk()
    mainFunction()
    
def mainFunction():
    setInitialValues()
    introScreen()
    runGame(level)
    
def clicked( event ):
    global w, h, level, startGame
    
    xMouse, yMouse = event.x, event.y

    if sw/2 - w < xMouse <  sw/2 + w and sh*2/5 - h < yMouse < sh*2/5 + h:
        showInstruction()
        startGame =  False
        
    elif sw/2 - w < xMouse < sw/2 + w and sh*3/5 - h < yMouse < sh*3/5 + h:
        promptForLevel()
             
# Main
root = tk.Tk()
mainFunction()
root.mainloop()
