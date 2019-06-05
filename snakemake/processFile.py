import json
import requests as req

def processFile(input):
    file = open(input,"r")
    jsonFile = json.load(file)
    for mutations in jsonFile:
        url = 'http://192.168.1.101/value=1'
        resp = req.get(url)
        results = resp.text
        for repl in ["'","[","]","[","]"]:
            results = results.replace(repl,"")
        results = results.split(",")
        print(results)

processFile("example.json")