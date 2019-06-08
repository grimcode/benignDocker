# Author: Alex Janse
# Version: 1.0
# Date: June 2019
# Description: Function to filter out the benign mutations.
import json

def filterBenign(input, output):

    file = json.load(open(input,"r"))
    filteredData = []

    for mutation in file:
        keep = True
        if not mutation['benign']:
            print(mutation['benign'])
            keep = False

        if keep:
            print("check")
            filteredData.append(mutation)
    print(filteredData)
    outputFile = json.load(open(output,"w+"))
    json.dump(filteredData, outputFile, indent=4)
