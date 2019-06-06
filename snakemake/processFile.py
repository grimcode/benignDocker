import json
import requests as req

def processFile(input, output):
    file = open(input,"r")
    jsonFile = json.load(file)
    resultList = []

    for mutations in jsonFile:

        url = 'http://172.17.0.3:5000/{}/{}/{}'.format(mutations["chr"].split("chr")[1],mutations["pos"],mutations["var"])
        resp = req.get(url)
        results = resp.text

        if results.startswith("['<!DOCTYPE HTML PUBLIC"):
            raise ValueError
        elif not results.startswith("()"):
            for repl in ["'","[","]","{","}"]:
                results = results.replace(repl,"")
            results = results.split(",")
            resultDict = {}
            for result in results:
                keyValue = result.split(":")
                value = convertValue(keyValue[0].strip(), keyValue[1].strip(), resultDict)

            resultDict["inDB"] = True
            resultList.append(resultDict)
            
        else:
            resultList.append(addNonDbMutation(mutations))

    outputFile = open(output,"w+")
    json.dump(resultList, outputFile)
    outputFile.close()

def convertValue(key, value, dict):
    keyDict = {
        "REFERENCE"     : "ref",
        "variant"       : "var",
        "name"          : "chrom",
        "ID"            : "GnomAd_ID"
    }
    if key in keyDict.keys():
        key = keyDict[key]

    if key in ["pos","cancerCount","cancerTotal","allelCount","allelTotal"]:
        value =  int(value)
    elif key == "benign":
        if value == "0":
            value = False
        elif value == "1":
            value = True
        else:
            raise ValueError

    if value == "":
        value = "NA"
    if key != "chromID": # Filterout the SQL IDs
        dict[key] = value

    return dict

def addNonDbMutation(mutation):
    return {
        "ref"           : mutation["ref"],
        "var"           : mutation["var"],
        "pos"           : mutation["pos"],
        "chr"           : mutation["chr"],
        "cancerCount"   : "NA",
        "cancerTotal"   : "NA",
        "allelCount"    : "NA",
        "allelTotal"    : "NA",
        "GnomAd_ID"     : "NA",
        "benign"        : False,
        "inDB"          : False
    }

processFile("example.json","test.json")
