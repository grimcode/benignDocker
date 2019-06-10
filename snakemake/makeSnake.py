# Made by: Alex Janse
# 29-05-2019
# Version: 0.1
# Description: Function to build the snakefile.
import json
from datetime import date
import sys
import ast

def makeSnake(input,output,report = None,cancerOnly = False):
    if report == "None":
        report = None
    workflow = "workflows/workflow"+date.today().strftime("_%B_%d_%Y")+".svg"

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
    "\t\t\"{}\"\n".format(workflow)+
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
    reportSnake+
    "\nrule makeWorkflow:\n"
    "\tinput:\n"
    "\t\t\"{}\",\n"
    "\toutput:\n"
    "\t\t\"{}\"\n"
    "\tshell: \"snakemake --dag -s Snakefile | dot -Tsvg > {} | echo \'BenignDbApp is finished. Checkout the workflow directory for an overview of the runned workflow. The error below is safe and will not have inpact on the results.\'\"".format(goal,workflow,workflow)
    )
    snakefile.close()

# processFile("example.json","test.json")
makeSnake(sys.argv[1],sys.argv[2],sys.argv[3],ast.literal_eval(sys.argv[4]))
