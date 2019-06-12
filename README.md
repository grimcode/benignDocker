# Welcome to BenignNoMore!

## Summary:
BenignNoMore is a state of the art application that is able to filter out benign human DNA mutations from a JSON file.

## Requirements:
OS:
- Ubuntu  
  
Software:
- docker
- python3
- snakemake
- graphviz

## Usage:
To install the application please use the INSTALL bash script. This script will use docker to build the containers and run them.  
This is important to use to make sure it is proper installed.  
```bash
./INSTALL
```  
   
When the containers are running, please use the TESTME bash script located in the snakemake directory.  
This script serves as a check to make sure that everything is working as it should.  
```bash  
./snakemake/TESTME
```  
If errors are given, please make sure that the API and database containers are up and running.  

When error free you can use the USEME script located in the snakemake directory.  
For first time use, feel free to use the -h argument to get information about the necessary arguments.  
```bash  
./snakemake/USEME -h
```  
For an example of an input, please check the example.json located in the snakemake/testFiles directory.  
```bash  
cat ./snakemake/testFiles/example.json
```  
Please be aware that the main keys ("0","1"...etc) are arbitrair and serves no role in this application but are necesary for the JSON importers.

## Expanding the db
For now only chromosome 21 mutations are present in the database. When other data is required make sure that the benign container are removed 
from docker before moving on. Then you can use the buildInsertDataFile() function of the build_SQL_file.py in the database directory with as 
argument the path to the vcf file. After running this function you should be able to use the INSTALL script to proceed as normal.
