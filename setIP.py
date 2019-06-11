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
