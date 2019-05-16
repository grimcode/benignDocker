

# Function to create a SQL file for filling the database
def buildInsertDataFile(vcfPath,output = "insertData.sql"):

    file = open(vcfPath,"r")
    outputFile = open(output,"w+")

    for line in file:
        lineParts = line.split("\t")
