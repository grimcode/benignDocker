import json

def processFile(input):
    file = open(input,"r")
    jsonFile = json.load(file)
    


processFile("example.json")