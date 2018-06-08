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


def end(event):
    root.destroy()
    exit()   

def runGame():

    escapeText = canvas.create_text(sw/2, 50, text="Press \"ESC\" to end session", font="Helvetica 12", fill="white")

runGame()

##canvas.bind("<Button-1>", click)
canvas.bind("<Escape>", end)
canvas.focus_set()
