# Made by: Alex Janse
# 29-05-2019
# Version: 0.1
import json

def makeSnake(input,output):

    snakefile = open("Snakefile","w+")
    snakefile.write(
    "rule all:\n"
    "\tinput:\n"
    "\t\t\"{}\"\n"
    "\n"
    "#rule viewWorkflow:\n"
    "\n"
    "\n"
    "rule addMetaData:\n"
    "\tinput:\n"
    "\t\t\"{}\"\n"
    "\toutput:\n"
    "\t\t\"{}\"\n"
    "\tshell:\n"
    "\t\t\"python3 -c 'import metaDataMiner as mdm; mdm.processFile(\\\"{{input}}\\\",\\\"{{output}}\\\")'\"\n".format(output,input,output)

    # rule filterBenign:

    # rule makeReport:'"
    )
    snakefile.close()

# processFile("example.json","test.json")
makeSnake("example.json","test.json")
