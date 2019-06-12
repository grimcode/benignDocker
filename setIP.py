#############################################
# Author: Alex Janse                        #
# Date: June 2019                           #
# Version: 1.0                              #
# Description: Script to set the database   #
# 	       container IP in the .env     #
#  	       file which is needed for     #
#	       the api container.	    #
#############################################
import sys

ip = sys.argv[1]
file = open("./api/.env","r")
new = ""
for rule in file:
    if rule.startswith("HOST="):
        new += "HOST=\""+ip+"\"\n"
    else:
        new += rule
file.close()
file = open("./api/.env","w")
file.write(new)
file.close()
