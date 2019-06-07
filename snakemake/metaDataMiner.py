# Author: Alex Janse
# Version: 1.0
# Date: June 2019
# Description: Contains functions that are called by snakemake to add metadata to a mutation json file.
import json
import requests as req
import re
import multiprocessing as mp

def processFile(input, output):
    file = open(input,"r")
    jsonFile = json.load(file)
    resultList = []

    units = mp.cpu_count()
    print(units)
    with mp.Pool(processes = units) as p:
        resultList.append(p.map(getMetaData,[mutations for mutations in jsonFile]))
    outputFile = open(output,"w+")
    json.dump(resultList[0], outputFile, indent=4)
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

def getMetaData(mutations):
    url = 'http://172.17.0.3:5000/?chromID={}&position={}&reference={}&variant={}'.format(mutations["chr"].split("chr")[1],mutations["pos"],mutations["ref"],mutations["var"])
    resp = req.get(url)
    results = resp.text
    if re.search("DOCTYPE",results) is not None:
        print("Could not find IP-address of API container!")
        raise ValueError
    elif not results.lower().startswith("uw"):
        for repl in ["'","[","]","{","}"]:
            results = results.replace(repl,"")
        results = results.split(",")
        resultDict = {}
        for result in results:
            keyValue = result.split(":")
            value = convertValue(keyValue[0].strip(), keyValue[1].strip(), resultDict)

        resultDict["inDB"] = True
        return(resultDict)

    else:
        return(addNonDbMutation(mutations))
