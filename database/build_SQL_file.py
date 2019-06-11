

# Function to create a SQL file for filling the database
def buildInsertDataFile(vcfPath,
                        output = "insertData.sql"):

    file = open(vcfPath,"r")
    outputFile = open(output,"w+")

    addChromosomes(outputFile)
    addMutations(file,outputFile)
    outputFile.write("COMMIT;")

# Function to add queries for adding chromosomes to the Chromosome Table
def addChromosomes(outputFile):

    for chrom in [[1,"1"],  [2,"2"],  [3,"3"],  [4,"4"],  [5,"5"],
                  [6,"6"],  [7,"7"],  [8,"8"],  [9,"9"],  [10,"10"],
                  [11,"11"],[12,"12"],[13,"13"],[14,"14"],[15,"15"],
                  [16,"16"],[17,"17"],[18,"18"],[19,"19"],[20,"20"],
                  [21,"21"],[22,"22"],[23,"x"], [24,"y"]]:
        outputFile.write(
            "INSERT INTO Chromosomes VALUES({} ,\"{}\");\n".format(chrom[0],chrom[1])
        )


# Function to add queries for adding the data in the file to the Mutations Table
def addMutations(file,outputFile):
    idList = {}
    
    for line in file:
        if not line.startswith("#"):
            lineParts = line.split("\t")
            if lineParts[6] == "PASS":
                chrom = convertChromToId(lineParts[0])
                pos = int(lineParts[1])
                id = lineParts[2]
                    
                if id in idList.keys():
                        idList[id] = idList[id]+1
                        id = id + "." + str(idList[id])
                else:
                    idList[id] = 1
                    id += ".1"
            
                ref = lineParts[3]
                alt = lineParts[4]
                qual = lineParts[5]
                count, total, cancerCount, cancerTotal = extractFromMeta(lineParts[7])
                if (count / total * 100) > 1:
                    benign = 1
                else:
                    benign = 0
                if len(ref) < 100 or len(var) < 100:
                    outputFile.write(
                        "INSERT INTO Mutations VALUES (\"{}\",{},{},"
                        "\"{}\",\"{}\",{},{},{},{},{},{});\n".format(id,chrom,pos,
                                                      ref,alt,qual,
                                                      count,total,benign,
                                                      cancerCount,cancerTotal)
                )


# Function to convert chromosome annotation to the chromsome ID
def convertChromToId(chrom):
    try:
        return int(chrom)
    except ValueError as e:
        if chrom.lower() == "x":
            return 23
        elif chrom.lower() == "y":
            return 24
        else:
            raise ValueError

# Function to extract the desired data from the metadata in the file
def extractFromMeta(meta):
    data = meta.split(";")
    count = int(data[0].split("=")[1])
    total = int(data[1].split("=")[1])

    noncancerCount = 0
    noncancerTotal = 0
    for item in data:

        if item.startswith("non_cancer_AC_female") or \
                item.startswith("non_cancer_AC_male"):
            noncancerCount += int(item.split("=")[1])

        elif item.startswith("non_cancer_AN_female") or \
                item.startswith("non_cancer_AN_male"):
            noncancerTotal += int(item.split("=")[1])
    cancerCount = count - noncancerCount
    cancerTotal = total - noncancerTotal

    if cancerCount < 0 or cancerTotal < 0 or cancerCount > cancerTotal:
        raise ValueError

    return count,total,cancerCount,cancerTotal



buildInsertDataFile()
