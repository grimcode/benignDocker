#################################################
# Author: Alex Janse                            #
# Date: June 2019                               #
# Version: 1.0                                  #
# Description: Function to make a report out of #
#              the results from dataFilter.py   #
#################################################
import json
from datetime import date
import os

# Main like function
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
    title = "<!DOCTYPE html>\n<h1>Benign Report: "+date.today().strftime("%B %d, %Y")+"</h1>"
    description = "<p>The following report shows the results after " \
                  "filtering out the benign mutations from " + \
                  original.split(os.sep)[-1] + ".</p>"
    summary = "<p>From the " + str(startlen) + " sequences submitted " + str(startlen - endlen) + \
              " turned out to be benign and were filtered out.<br>In " \
              "the results below you can find the non-benign mutations<br></p><br>"

    return title+description+summary

def addTable(results):
    attributes = ["chrom","pos","ref","var","GnomAd_ID","quality","allelCount","allelTotal","allelFreq","cancerCount","cancerTotal","inDB","isBenign"]
    table = "<section><div style = \"overflow:auto; position: relative; width: 1400px; height : 500px\">"\
            "<table>\n<thead>\n<tr>\n"
    for header in attributes+["GnomadURL"]:
        table += "<th><b><ins>"+header+"</ins></b></th>\n"
    table += "</tr>\n</thead>\n<tbody>\n"

    for result in results.values():
            table += "<tr>\n"
            for att in attributes:
                if att == "allelFreq" and isinstance(result[att], float):
                    table += "<th>{0:.4g}</th>\n".format(result[att])
                else:
                    table += "<th>"+str(result[att])+"</th>\n"
            if str(result["inDB"]) != "False":
                table += "<th><a href=\"https://gnomad.broadinstitute.org/variant/"+str(result["chrom"])+"-"+ \
                str(result["pos"])+"-"+str(result["ref"])+"-"+str(result["var"])+"\" target = \"_blank\">See GnomAd page</a></th>\n"
            else:
                table += "<th>NA</th>\n"

            table += "</tr>\n"
    table += "</tbody>\n</table>\n</div></section>"
    return table
