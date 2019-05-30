import json
from datetime import date
import os

def createReport(original,result,html = True):

    originalFile = json.load(open(original,"r"))
    resultFile = json.load(open(result,"r"))
    startlen = len(originalFile)
    endlen = len(resultFile)
    outputText = addIntro(html, original, startlen, endlen)


def addIntro(html,original, startlen, endlen):
    title = "Benign Report: "+date.today().strftime("%B %d, %Y")
    description = "The following report shows the results after " \
                  "filtering out the benign mutations from " + \
                  original.split(os.sep)[-1] + "."
    summary = "From the " + startlen + " sequences " + startlen - endlen + \
              " turned out to be benign and were filtered out."
    content = "1. Cancer Mutations\n2. All Non-Benign Mutations"


