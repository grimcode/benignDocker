import json
import requests as req

def processFile(input, output):
    file = open(input,"r")
    jsonFile = json.load(file)
    resultList = []

    for mutations in jsonFile:
        url = 'http://172.17.0.3:5000/21/11085688/C'
        resp = req.get(url)
        results = resp.text
        for repl in ["'","[","]","{","}"]:
            results = results.replace(repl,"")
        results = results.split(",")

        resultDict = {}
        for result in results:
            keyValue = result.split(":")
            value = convertValue(keyValue[0].strip(), keyValue[1].strip(), resultDict)
        resultList.append(resultDict)

    outputFile = open(output,"w+")
    json.dump(resultList, outputFile)
    outputFile.close()

def convertValue(key, value, dict):
    keyDict = {
        "REFERENCE"     : "ref",
        "variant"       : "alt",
        "name"          : "chrom",
        "ID"            : "GnomAd_ID",
    }
    if key in keyDict.keys():
        key = keyDict[key]
    if key in ["pos","cancercount","cancerTotal","allelCount","allelTotal"]:
        value =  int(value)
    if key != "chromID" and not key.startswith(".."): # Filterout the SQL IDs and unknown GnomAd_ID
        dict[key] = value

    return dict
