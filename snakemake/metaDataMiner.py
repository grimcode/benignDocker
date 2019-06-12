#########################################################
# Author: Alex Janse                                    #
# Version: 1.0                                          #
# Date: June 2019                                       #
# Description: Contains functions that are called by    #
#              snakemake to add metadata to a mutation  #
#              json file.                               #
#########################################################
import json
import requests as req
import re
import multiprocessing as mp

# Loop parallel over the file and process the results
def processFile(input, output,cancerOnly, ip):

    jsonFile = json.load(open(input,"r"))

    units = mp.cpu_count() # Counts the number of CPU cores
    with mp.Pool(processes = units) as p:
        results = (p.map(getMetaData,[[mutations,cancerOnly, ip] for mutations in jsonFile.values()]))

    count = 0
    resultDict = {}
    for result in results:
        if result is not None:
            resultDict[str(count)] = result
            count += 1

    outputFile = open(output,"w+")
    json.dump(resultDict, outputFile, indent=4)
    outputFile.close()

# Adjust the results from the database
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

    if key in ["pos","cancerCount","cancerTotal","allelCount","allelTotal","chrom"]:
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

    if key == "chrom":
        if value != 21:
            print("WARNING: THE DATABASE ONLY CONTAINS MUTATIONS OF CHROMOSOME 21."
		  "Cause error: found mutation with chr"+str(value))
    elif key == "ref" or ket == "var":
        if len(value) > 100:
            print("WARNING: THE DATABASE ONLY CONTAINS MUTATIONS WITH A MAXIMUM LENGTH OF 100 CHARACTERS AS REFERENCE OR VARIANT NUCLEOTIDES."
                  "Cause error: found mutation with as "+key+": "+value+" which has a length of "+len(value)+".\n")
    if key == "GnomAd_ID":
        value = value.split(".")[0]

    if value == "":
        value = "NA"

    if key != "chromID": # Filterout the SQL IDs
        dict[key] = value

    return dict

# Add unknown mutation to the results
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

# Process the database results
def getMetaData(data):
    mutations = data[0]
    cancerOnly = data[1]
    ip = data[2]

    url = 'http://'+ip+':5000/?chromID={}&position={}&reference={}&variant={}&cancer={}'.format(mutations["chr"].split("chr")[1],mutations["pos"],mutations["ref"],mutations["var"],cancerOnly)
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

    elif not cancerOnly:
        return(addNonDbMutation(mutations))
