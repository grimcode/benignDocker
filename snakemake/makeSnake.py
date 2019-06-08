# Made by: Alex Janse
# 29-05-2019
# Version: 0.1
import json

def makeSnake(input,output,report = None,cancerOnly = False):
    if report is None:
        goal = output
        reportSnake = "\n"
    else:
        goal = report
        reportSnake = "\nrule makeReport:\n" \
                      "\tinput:\n" \
                      "\t\toriginal=\"{}\",\n" \
                      "\t\tresults=\"{}\"\n" \
                      "\toutput:\n" \
                      "\t\t\"{}\"\n" \
                      "\tshell:\n" \
                      "\t\t\"python3 -c 'import report as rp; rp.createReport(\\\"{{input.original}}\\\",\\\"{{input.results}}\\\",\\\"{{output}}\\\")'\"\n".format(input,output,report)

    snakefile = open("Snakefile","w+")
    snakefile.write(
    "rule all:\n"
    "\tinput:\n"
    "\t\t\"{}\"\n".format(goal)+
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
    "\t\t\"python3 -c 'import metaDataMiner as mdm; mdm.processFile(\\\"{{input}}\\\",\\\"{{output}}\\\",{})'\"\n"
    "\n"
    "rule filterBenign:\n"
    "\tinput:\n"
    "\t\t\"{}\"\n"
    "\toutput:\n"
    "\t\t\"{}\"\n"
    "\tshell:\n"
    "\t\t\"python3 -c 'import dataFilter as df; df.filterBenign(\\\"{{input}}\\\",\\\"{{output}}\\\")'\"\n"
    "\n".format(input,"tempOutput.json",cancerOnly,"tempOutput.json",output)+
    reportSnake
    )
    snakefile.close()

# processFile("example.json","test.json")
makeSnake("example.json","test.json","test.html")
