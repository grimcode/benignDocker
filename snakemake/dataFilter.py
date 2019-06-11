#############################################################
# Author: Alex Janse                                        #
# Version: 1.0                                              #
# Date: June 2019                                           #
# Description: Function to filter out the benign mutations. #
#############################################################
import json

def filterBenign(input, output):
    file = json.load(open(input,"r"))
    filteredData = {}
    count = 0
    for mutation in file.values():
        keep = True
        if mutation['isBenign']:
            keep = False

        if keep:
            filteredData[str(count)] = mutation
            count += 1

    outputFile = open(output,"w+")
    json.dump(filteredData, outputFile, indent=4)
