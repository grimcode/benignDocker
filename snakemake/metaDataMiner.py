# Author: Alex Janse
# Version: 1.0
# Date: June 2019
# Description: Contains functions that are called by snakemake to add metadata to a mutation json file.
import json
import requests as req
import re
import multiprocessing as mp

def processFile(input, output,cancerOnly):
    file = open(input,"r")
    jsonFile = json.load(file)

    units = mp.cpu_count()
    with mp.Pool(processes = units) as p:
        results = (p.map(getMetaData,[[mutations,cancerOnly] for mutations in jsonFile.values()]))

    count = 0
    resultDict = {}
    for result in results:
        resultDict[str(count)] = result
        count += 1

    outputFile = open(output,"w+")
    json.dump(resultDict, outputFile, indent=4)
    outputFile.close()

def convertValue(key, value, dict):
    keyDict = {
        "REFERENCE"     : "ref",
        "variant"       : "var",
        "name"          : "chrom",
        "ID"            : "GnomAd_ID",
        "benign"        : "isBenign",
        "position"      : "pos",
        "qual"          : "quality"
    }
    if key in keyDict.keys():
        key = keyDict[key]

    if key in ["pos","cancerCount","cancerTotal","allelCount","allelTotal"]:
        value =  int(value)
    elif key == "quality":
        value = float(value)
    elif key == "isBenign":
        if value == "0":
            value = False
        elif value == "1":
            value = True
        else:
            raise ValueError
    if key == "GnomAd_ID":
        value = value.split(".")[0]

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
        "chrom"         : mutation["chr"].split("chr")[1],
        "cancerCount"   : "NA",
        "cancerTotal"   : "NA",
        "allelCount"    : "NA",
        "quality"       : "NA",
        "allelTotal"    : "NA",
        "GnomAd_ID"     : "NA",
        "isBenign"      : False,
        "inDB"          : False,
        "allelFreq"     : "NA"
    }

def getMetaData(data):
    mutations = data[0]
    cancerOnly = data[1]

    url = 'http://172.17.0.3:5000/?chromID={}&position={}&reference={}&variant={}&cancer={}'.format(mutations["chr"].split("chr")[1],mutations["pos"],mutations["ref"],mutations["var"],cancerOnly)
    resp = req.get(url)
    results = resp.text

    if re.search("DOCTYPE",results) is not None:
        print("Could not find IP-address of API container!")
        raise ValueError
    elif results != "None":
        for repl in ["'","[","]","{","}"]:
            results = results.replace(repl,"")
        results = results.split(",")
        resultDict = {}
        for result in results:
            keyValue = result.split(":")
            value = convertValue(keyValue[0].strip(), keyValue[1].strip(), resultDict)

        resultDict["inDB"] = True
        try:
            resultDict["allelFreq"] = resultDict["allelCount"] / resultDict["allelTotal"]
        except Exception as e:
            resultDict["allelFreq"] = "NA"

        return(resultDict)

    else:
        return(addNonDbMutation(mutations))
