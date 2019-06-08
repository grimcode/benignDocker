import json
from datetime import date
import os

def createReport(original,result,output):

    originalFile = json.load(open(original,"r"))
    resultFile = json.load(open(result,"r"))
    startlen = len(originalFile)
    endlen = len(resultFile)
    outputText = addIntro(original, startlen, endlen)
    outputText += addTable(resultFile)
    outputFile = open(output,"w+")
    outputFile.write(outputText)
    outputFile.close()

def addIntro(original, startlen, endlen):
    title = "<h1>Benign Report: "+date.today().strftime("%B %d, %Y")+"</h1><br>"
    description = "<p>The following report shows the results after " \
                  "filtering out the benign mutations from " + \
                  original.split(os.sep)[-1] + ".</p><br>"
    summary = "<p>From the " + str(startlen) + " sequences " + str(startlen - endlen) + \
              " turned out to be benign and were filtered out. In " \
              "the results below you can find the non-benign mutations " \
              "that were found in cancer patients and the non-benign " \
              "mutations found in both cancer as non-cancer patients.</p><br>"

    return title+description+summary

def addTable(results):
    attributes = ["chrom","pos","ref","var","GnomAd_ID","quality","allelCount","allelTotal","allelFreq","cancerCount","cancerTotal","inDB","isBenign"]
    table = "<table align = "right" style\"width:100%\">\n<tr>\n"
    for header in attributes:
        table += "<th><b><ins>"+header+"</insr></b></th>\n"
    table += "</tr>\n"
    for result in results.values():
        table += "<tr>\n"
        for att in attributes:
            table += "<th>"+str(result[att])+"</th>\n"
        table += "</tr>\n"
    return table
