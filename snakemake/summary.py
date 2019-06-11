#########################################################
# Author: Alex Janse                                    #
# Date: June 2019                                       #
# Version: 1.0                                          #
# Description: Function to get the summary of results   #
#########################################################
import json

def getSummary(input, output, original):
    inputFile = json.load(open(input,"r"))
    originalFile = json.load(open(original,"r"))
    startLen = len(originalFile)
    endLen = len(inputFile)
    cancerCount, snpCount, indelCount, restCount = getCounts(inputFile)

    outputFile = open(output,"w+")
    outputFile.write(
    "Summary:"
    "\nNumber of submitted mutations\t\t\t\t= "+str(startLen)+\
    "\nNumber of non-benign mutations\t\t\t\t= "+str(endLen)+\
    "\nNumber of non-benign mutations found in cancer patients\t= "+str(cancerCount)+\
    "\nNumber of non-benign SNPs\t\t\t\t= "+str(snpCount)+\
    "\nNumber of non-benign indels\t\t\t\t= "+str(indelCount)+\
    "\nNumber of non-benign other type of mutations\t\t= "+str(restCount)+"\n\n"
    )
    outputFile.close()

def getCounts(inputFile):
    cancerCount = 0
    snpCount = 0
    indelCount = 0
    restCount = 0
    for result in inputFile.values():
        if str(result["cancerCount"]) != "NA":
            if int(result["cancerCount"]) > 0:
                cancerCount += 1
        if len(result["ref"]) == 1 and len(result["var"]) == 1:
            snpCount += 1
        elif len(result["ref"]) != len(result["var"]):
            indelCount += 1
        else:
            restCount += 1
    return cancerCount, snpCount, indelCount, restCount
