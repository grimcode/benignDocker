# Made by: Alex Janse
# 29-05-2019
# Version: 0.1
import json

def makeSnake(input):

    snakefile = open("Snakefile","w+")
    inputfile = json.load(open(input,"r"))

