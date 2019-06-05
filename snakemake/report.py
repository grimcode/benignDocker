import json
from datetime import date
import os

def createReport(original,result,html = True):

    originalFile = json.load(open(original,"r"))
    resultFile = json.load(open(result,"r"))
    startlen = len(originalFile)
    endlen = len(resultFile)
    outputText = addIntro(html, original, startlen, endlen)
    #outputText = addCancer(resultFile,outputText)

    return outputText

def addIntro(html,original, startlen, endlen):
    title = "Benign Report: "+date.today().strftime("%B %d, %Y")
    description = "The following report shows the results after " \
                  "filtering out the benign mutations from " + \
                  original.split(os.sep)[-1] + "."
    summary = "From the " + str(startlen) + " sequences " + str(startlen - endlen) + \
              " turned out to be benign and were filtered out. In " \
              "the results below you can find the non-benign mutations " \
              "that were found in cancer patients and the non-benign " \
              "mutations found in both cancer as non-cancer patients."
    content = "1. Cancer Mutations\n2. All Non-Benign Mutations"

    if html:
        title = "<h1>"+title+"</h1>"
        description = "<br><p>"+description+"</p>"
        summary = "<p>"+summary+"</p>"
        content = "<ul>" \
                  "<li><a href=\"#cancer\">Cancer Mutation</a></li>" \
                  "<li><a href=\"#all\">All Non-Benign Mutations</a></li>" \
                  "</ul>"
        return title+description+summary+content
    else:
        return title+"\n"+description+"\n"+summary+"\n"+content+"\n"


def addCancer(results,text,html):
    for result in results:
        if int(result['cancerCounts']) > 0:
            if html:
                print()