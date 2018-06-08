######################################################################
# __        _____  ____  ____    __  __    _  _____ ____  _____  __  #
# \ \      / / _ \|  _ \|  _ \  |  \/  |  / \|_   _|  _ \|_ _\ \/ /  #
#  \ \ /\ / / | | | |_) | | | | | |\/| | / _ \ | | | |_) || | \  /   #
#   \ V  V /| |_| |  _ <| |_| | | |  | |/ ___ \| | |  _ < | | /  \   #
#    \_/\_/  \___/|_| \_\____/  |_|  |_/_/   \_\_| |_| \_\___/_/\_\  #                                                               
#                                                    By: David Chen  #
######################################################################


# Imports
from tkinter import *
from random import *
from time import *


# Tkinter set-up
root = Tk()
root.title("WORD MATRIX")
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.attributes('-fullscreen', True)
canvas = Canvas(root, width=sw, height=sh, highlightthickness=0, bg="black")
canvas.pack()


# Global variables that are commonly used by other functions
def globalVariables():
    global difficulty, score, lives, mistake, fallSpeed, genSpeed, hearts, words, text, x, y, displayHealth, inputBar,\
           displayInput, displayScore, heartImage, healthText, startGame, missedWord, wrongWord, correct, titleImage

    # Easy, Medium, Hard, Extreme
    difficulty = ""

    # Result variables
    score = 0
    lives = 10
    missedWord = 0
    wrongWord = 0
    correct = 0

    # Flags
    mistake = False
    startGame = False
    disableInput = False

    # Empty arrays 
    hearts = []
    words = []
    text = []
    x = []
    y = []
    displayHealth = []

    # Empty variables
    inputBar = ""
    displayInput = None
    displayScore = None
    healthText = None

    # Fills hearts array with the number of default lives
    heartImage = PhotoImage(file="Resources/Heart.gif")
    for i in range(lives):
        heart = canvas.create_image((sw-25)-(i*30), 50, image=heartImage)
        canvas.delete(heart)
        hearts.append(heart)

    # Title image
    titleImage = PhotoImage(file="Resources/title.gif")


# Picks a random word from dictionary.txt
def pickWord():
    line = choice(open("Resources/dictionary.txt").readlines()).replace("\n", "")
    return line


# Generates a new word
def dropNewWord():
    xPos, yPos = randint(0, sw), -40
    pick = pickWord()
    text.append(pick)
    
    # Makes sure the words aren't generated off the screen
    if xPos > sw/2:
        word = canvas.create_text(xPos, yPos, text=pick, font="Helvetica 50", fill="yellow", anchor=E)
    else:
        word = canvas.create_text(xPos, yPos, text=pick, font="Helvetica 50", fill="yellow", anchor=W)

    canvas.delete(word)
    x.append(xPos)
    y.append(yPos)
    words.append(word)


# Shifts an already-generated word downwards
def updateWord(i):
    y[i] += fallSpeed

    # Makes sure the words aren't generated off the screen
    if x[i] > sw/2:
        words[i] = canvas.create_text(x[i], y[i], text=text[i], font="Helvetica 50", fill="yellow", anchor=E)
    else:
        words[i] = canvas.create_text(x[i], y[i], text=text[i], font="Helvetica 50", fill="yellow", anchor=W)


# Checks if the user input matches a word that has been generated
def match(a, b):
    global score, lives, mistake, correct

    # Deletes word off screen, and adds 100 points to the score
    if a == b:
        index = text.index(b)
        canvas.delete(words[index])
        del x[index], y[index], text[index], words[index]
        score += 100
        correct += 1
        return True

    # Input doesn't match a word on screen
    else:
        mistake = True
        return False


# Takes user input
def userInput(event):
    global inputBar, displayInput, disableInput, wrongWord, score

    # Allows user to enter in the input bar
    if disableInput == False:

        # List of the characters that are acceptable as input
        alphabetLowercase = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                             "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        alphabetUppercase = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                             "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        
        letter = event.keysym

        # If return key is pressed, send word to match(a, b)
        if letter == "Return" or letter == "space":
            skip = False

            # Iterates through each word on-screen
            for word in text:
                matchVar = match(inputBar, word)

                # Breaks the loop if the user's input matches a word on-screen
                if matchVar == True:
                    break

                # Makes sure this block is only run once during the loop
                elif matchVar == False and skip == False: 
                    wrongWord += 1
                    score -= 200
                    skip = True

            # Resets input bar        
            inputBar = ""

        # If backspace key is pressed, delete previous character
        elif letter == "BackSpace":
            inputBar = inputBar[:-1]

        # If a character from the alphabet is pressed, display character on screen
        else:
            if letter in alphabetLowercase or letter in alphabetUppercase:
                inputBar += letter

        canvas.delete(displayInput)
        displayInput = canvas.create_text(100, sh-50, text=inputBar, anchor=W, font="Helvetica 24", fill="green")


# Clear all of the input bar
def clearInput(event):
    global inputBar, displayInput
    
    inputBar = ""
    canvas.delete(displayInput)
    displayInput = canvas.create_text(100, sh-50, text=inputBar, anchor=W, font="Helvetica 24", fill="green")


# Displays the score
def showScore():
    global displayScore
    
    canvas.delete(displayScore)
    displayScore = canvas.create_text(50, 50, text="Score: " + str(score), font="Helvetica 24", fill="sky blue", anchor=W)


# Displays the remaining health
def showHealth():
    global lives, hearts, mistake, healthText

    canvas.delete(healthText)
    healthText = canvas.create_text(sw-50, 50, text="Health: " + str(lives), font="Helvetica 24", fill="sky blue", anchor=E)
    
    for i in range(lives):
        canvas.delete(hearts[i])

    # If a mistake was made in match(a, b), delete a heart from the screen
    if mistake == True:
        lives -= 1
        mistake = False

    # Generates the heart images
    for i in range(lives):
        hearts[i] = canvas.create_image((sw-25)-(i*30), 85, image=heartImage)


# Displays the countdown
def countdown():
    numbers = ["3", "2", "1", "GO"]
    i = 0
    
    for number in numbers:
        
        # After 1000 frames, print the next number
        while i % 1000 != 1:
            i += 1
            displayNumber = canvas.create_text(sw/2, sh/2, text=number, font="Helvetica 50 bold", fill="white")
            canvas.update()
            sleep(0.5)
            canvas.delete(displayNumber)

        i = 0


# YOU MAY HAVE TO MODIFY THE GENSPEED AND FALLSPEED BASED ON THE COMPUTER'S SPEED.
# THE SPEEDS WERE DESIGNED TO WORK ON THE SCHOOL COMPUTERS.


# Click handler for menu()
def click(event):
    global difficulty, startGame, genSpeed, fallSpeed
    
    x, y = event.x, event.y

    # Detects if EASY is clicked
    if sw/2-100 < x < sw/2+100 and sh/2-100-50 < y < sh/2-100+50:
        difficulty = "Easy"
        fallSpeed = 0.2
        genSpeed = 1000
        startGame = True

    # Detects if MEDIUM is clicked
    if sw/2-150 < x < sw/2+150 and sh/2-50 < y < sh/2+50:
        difficulty = "Medium"
        fallSpeed = 0.4
        genSpeed = 500
        startGame = True

    # Detects if HARD is clicked
    if sw/2-100 < x < sw/2+100 and sh/2+100-50 < y < sh/2+100+50:
        difficulty = "Hard"
        fallSpeed = 0.8
        genSpeed = 300
        startGame = True

    # Detects if EXTREME is clicked
    if sw/2-175 < x < sw/2+175 and sh/2+200-50 < y < sh/2+200+50:
        difficulty = "Extreme"
        fallSpeed = 1.2
        genSpeed = 250
        startGame = True

    # Detects if EXIT is clicked
    if sw/2-100 < x < sw/2+100 and sh/2+350-50 < y < sh/2+350+50:
        end(True)
        

# Clears the game screen
def reset():
    global inputIndicator, displayHealth, displayScore, healthText, displayInput, x, y, text, words, hearts, escapeText
    
    canvas.delete(inputIndicator, escapeText, displayHealth, displayScore, healthText, displayInput)
    
    for i in range(len(hearts)):
        canvas.delete(hearts[i])

    x, y, text, words, hearts = [], [], [], [], []


# Displays game summary
def results():
    global startTime, endTime, score, wrongWord, missedWord, disableInput, n, lives, correct
    global resultText, wpmText, timeText, correctText, missedText, incorrectText, accuracyText, scoreText, menuText

    # Prevents user from entering in the input bar
    disableInput = True

    # Calculates result values
    totalTime = endTime - startTime
    wpm = int(correct / (totalTime / 60))
    accuracy = round(100-(missedWord+wrongWord)/(missedWord+wrongWord+correct)*100, 2)

    # Generates result text
    resultText = canvas.create_text(sw/2, sh/2-250, font="Helvetica 40", fill="white", text="RESULTS")
    wpmText = canvas.create_text(sw/2, sh/2-150, font="Helvetica 24", fill="white", text="Words per minute: " + str(wpm))
    timeText = canvas.create_text(sw/2, sh/2-100, font="Helvetica 24", fill="white", text="Time played: " + str(int(totalTime)) + " second(s)")
    correctText = canvas.create_text(sw/2, sh/2-50, font="Helvetica 24", fill="white", text="Words typed correctly: " + str(correct))
    missedText = canvas.create_text(sw/2, sh/2, font="Helvetica 24", fill="white", text="Words missed: " + str(missedWord))
    incorrectText = canvas.create_text(sw/2, sh/2+50, font="Helvetica 24", fill="white", text="Words typed incorrectly: " + str(wrongWord))
    accuracyText = canvas.create_text(sw/2, sh/2+100, font="Helvetica 24", fill="white", text="Accuracy: " + str(accuracy) + "%")
    scoreText = canvas.create_text(sw/2, sh/2+200, font="Helvetica 24 bold", fill="white", text="SCORE: " + str(score))
    
    canvas.update()

    # Infinite loop that waits for user input
    while True:
        menuText = canvas.create_text(sw/2, sh/2+350, text="MENU", font="Helvetica 50 bold", fill="white")
        canvas.update()
        sleep(0.1)
        canvas.delete(menuText)

        canvas.bind("<Button-1>", resultClick)
        canvas.focus_set()


# Click handler for results()
def resultClick(event):
    x, y = event.x, event.y

    # Detects if MENU is clicked
    if sw/2-100 < x < sw/2+100 and sh/2+350-50 < y < sh/2+350+50:
        resetResults()
        menu()


# Clears the result screen
def resetResults():
    global resultText, wpmText, timeText, missedText, incorrectText, menuText

    canvas.delete(resultText, wpmText, timeText, correctText, missedText, incorrectText, accuracyText, scoreText, menuText)


# Handler for <Escape>. Breaks the mainloop.
def escapeToMenu(event):
    global lives
    
    lives = 0
    return True


# Ends the program
def end(event):
    root.destroy()
    exit()    


# Main prodecure that runs the game
def runGame():

    # Displays the countdown
    countdown()
    
    # Initializes the global variables
    globalVariables()
    
    global lives, genSpeed, mistake, fallSpeed, startTime, endTime, n, missedWord, inputIndicator, disableInput, escapeText, score

    # Gets the starting time
    startTime = clock()

    # Allows user to enter in the input bar
    disableInput = False

    # Creates >> to indicate where the user's input will be shown
    inputIndicator = canvas.create_text(50, sh-50, text=">>", anchor=W, font="Helvetica 24", fill="red")
    escapeText = canvas.create_text(sw/2, 50, text="Press \"ESC\" to end session", font="Helvetica 12", fill="white")

    # Variable j keeps track of the frame number
    j = -1
    n = 0

    # Keep the game running until lives reach 0
    while lives > 0:
        j += 1

        # Speeds up the generation speed gradually
        if j % 500 == 0:
            if genSpeed > 25:
                genSpeed -= 1

        # Generates a new word based on the generation speed
        if j % genSpeed == 0:
            dropNewWord()
            n += 1

        # Shifts words downwards
        for i in range(len(words)):
            updateWord(i)

        # Updates score and health
        showScore()
        showHealth()
        
        canvas.update()
        sleep(0.0001)
        
        for i in range(len(words)):
            canvas.delete(words[i])

        # Handles words that are missed
        try:
            if y[j%len(words)] > sh+25:
                del x[j%len(words)], y[j%len(words)], text[j%len(words)], words[j%len(words)]
                missedWord += 1
                score -= 200
                mistake = True
        except:
            pass

        canvas.bind("<Key>", userInput)
        canvas.bind("<Escape>", escapeToMenu)
        canvas.bind("<Control-BackSpace>", clearInput)
        canvas.focus_set()

    # Gets the ending time
    endTime = clock()

    # Clears the screen, and displays the summary page
    reset()
    results()


# Main menu
def menu():  
    # Initializes the global variables
    globalVariables()
    
    global startGame, fallSpeed, genSpeed, disableInput, titleImage

    # Prevents user from entering in the input bar
    disableInput = True

    # Sets falling speed and generation speed
    fallSpeed = 2
    genSpeed = 100
    
    # Defines text variables
    titleText, easyText, mediumText, hardText, extremeText, quitText = None, None, None, None, None, None
    
    # Variable j keeps track of the frame number
    j = -1
    n = 0

    # Continues to animate the background if the user has not selected a difficulty
    while startGame == False:
        j += 1

        canvas.delete(titleText, easyText, mediumText, hardText, extremeText, quitText)

        # Generates a new word based on the generation speed
        if j % genSpeed == 0:
            dropNewWord()
            n += 1

        # Shifts words downwards
        for i in range(len(words)):
            updateWord(i)

        # Generates menu options text
        titleText = canvas.create_image(sw/2, sh/2-250, image=titleImage)
        easyText = canvas.create_text(sw/2, sh/2-100, text="EASY", font="Helvetica 50 bold", fill="green")
        mediumText = canvas.create_text(sw/2, sh/2, text="MEDIUM", font="Helvetica 50 bold", fill="orange")
        hardText = canvas.create_text(sw/2, sh/2+100, text="HARD", font="Helvetica 50 bold", fill="red")
        extremeText = canvas.create_text(sw/2, sh/2+200, text="EXTREME", font="Helvetica 50 bold", fill="blue")
        quitText = canvas.create_text(sw/2, sh/2+350, text="QUIT", font="Helvetica 50 bold", fill="white")
        
        canvas.update()
        sleep(0.0001)
        
        for i in range(len(words)):
            canvas.delete(words[i])

        # Handles words that are missed
        try:
            if y[j%len(words)] > sh+25:
                del x[j%len(words)], y[j%len(words)], text[j%len(words)], words[j%len(words)]
        except:
            pass

        canvas.bind("<Button-1>", click)
        canvas.bind("<Escape>", end)
        canvas.focus_set()

    # Starts the game after the mainloop is broken
    canvas.delete(titleText, easyText, mediumText, hardText, extremeText, quitText)    
    runGame()



# Calls the main procedure
menu()


