from tkinter import *
from math import *
from time import *
from random import *
import itertools

##root = Tk()
##s = Canvas(root, width=600, height=600, background="white")

file = open("out.txt", "w")
file.write("hi, ")
file.write("bye")


for x in range(100, 110):
    xVal = str(x)+ ", "
    yVal = str(x) + "\n"
    file.write(xVal)
    file.write(yVal)

file.close()
file = open("out.txt", "w")

for x in range(5):
    line = file.readlines()

print (line[4:6])
    
##    s.create_text(xCoor, yCoor, text = "hi", font = "Times 30", fill = "blue")
##    s.update()

##file = open("chineseCHAR.txt", encoding="utf8")
##line = choice(file.readlines()).replace("\n", "")
##print (line)

