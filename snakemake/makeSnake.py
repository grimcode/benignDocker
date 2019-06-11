#################################################
# Made by: Alex Janse                           #
# Date: 29-05-2019                              #
# Version: 0.1                                  #
# Description: Function to build the snakefile. #
#################################################
import json
from datetime import date
import sys
import ast

def makeSnake(input,output,report,cancerOnly, ip):
    if report == "None":
        report = None

    sum = "summaries/summary"+date.today().strftime("_%B_%d_%Y")+".svg" # The final file created in the workflow

    # determine if report is needed and if so change the goal variable to force sankemake to call getSummary at the end
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
    "\t\t\"{}\"\n".format(sum)+
    "\n"
    "rule addMetaData:\n"
    "\tinput:\n"
    "\t\t\"{}\"\n"
    "\toutput:\n"
    "\t\t\"tempOutput.json\"\n"
    "\tshell:\n"
    "\t\t\"python3 -c 'import metaDataMiner as mdm; mdm.processFile(\\\"{{input}}\\\",\\\"{{output}}\\\",{},\\\"{}\\\")'\"\n"
    "\n"
    "rule filterBenign:\n"
    "\tinput:\n"
    "\t\t\"tempOutput.json\"\n"
    "\toutput:\n"
    "\t\t\"{}\"\n"
    "\tshell:\n"
    "\t\t\"\"\"\n"
    "\t\tpython3 -c 'import dataFilter as df; df.filterBenign(\\\"{{input}}\\\",\\\"{{output}}\\\")',\n".format(input,cancerOnly,ip,output)+
    "\t\trm tempOutput.json\n"
    "\t\t\"\"\"\n"+
    reportSnake+
    "\nrule getSummary:\n"
    "\tinput:\n"
    "\t\tbait = \"{}\",\n" # File is not used but serves as bait to put this rule as last rule.
    "\t\tresults =\"{}\",\n"
    "\t\toriginal =\"{}\"\n"
    "\toutput:\n"
    "\t\t\"{}\"\n"
    "\tshell:\n"
    "\t\t\"python3 -c \'import summary as sm; sm.getSummary(\\\"{{input.results}}\\\",\\\"{{output}}\\\",\\\"{{input.original}}\\\")\' && cat {}\"\n".format(goal,output,input,sum, sum)
    )
    snakefile.close()

# Call function with the correct arguments from system
makeSnake(sys.argv[1],sys.argv[2],sys.argv[3],ast.literal_eval(sys.argv[4]),sys.argv[5])
