# Indicates that this is a python file.  
#!/usr/local/bin/python3
# The necessary imports to run this python file. 

# Module that handles url_requests. 
from flask import Flask, render_template,request
# Module that is being used to communicate with the database.
import pymysql
from dotenv import load_dotenv
import os
from os.path import join, dirname

# Make a connection to the database.
app = Flask(__name__)
dotenv_path=(join(dirname(__file__), './.env'))
print(dotenv_path)
load_dotenv(dotenv_path)
print(os.getenv("USER"))
con = pymysql.connect(host=os.getenv("HOST"), user=os.getenv("USER"), password=os.getenv("PASSWORD"), db=os.getenv("DATABASE"), cursorclass=pymysql.cursors.
                           DictCursor)

# Catches url_request arguments.
@app.route('/', methods=['GET', 'POST'])
def variants():
     chromID_user = request.args.get('chromID')
     if isinstance(chromID_user,str):
         if chromID_user.upper == 'X' or chromID_user.upper == 'Y':
                 chromID_user = chromo_dict(chromID_user)
     position_user = request.args.get('position')
     variant_user = request.args.get('variant')
     if isinstance(variant_user,str):
        variant_user = variant_user.upper()
     cancer = request.args.get('cancer')
     if isinstance(cancer,str):
        cancer = cancer.upper()

     reference_user = request.args.get('reference')
     if isinstance(reference_user,str):
        reference_user = reference_user.upper()

     if chromID_user is None or position_user is None or variant_user is None or reference_user is None:
        return ("Not all required arguments were given.")
     cur = con.cursor()
     #  Fetches data out of de database based on the arguments given in the request url.
     if (cancer is None or  cancer == 'N' or  cancer == 'NO' or cancer == False  or cancer == "FALSE" or cancer =="false" or cancer == "0"):
        query = "SELECT * FROM Mutations NATURAL JOIN Chromosomes WHERE Mutations.chromID = {} and Mutations.position ={} and variant = \"{}\" and Mutations.REFERENCE = \"{}\"".format(chromID_user,position_user,variant_user, reference_user)
     else:
        query = "SELECT * FROM Mutations NATURAL JOIN Chromosomes WHERE Mutations.chromID = {} and Mutations.position ={} and variant = \"{}\" and Mutations.REFERENCE = \"{}\" and cancerCount > 0".format(chromID_user,position_user,variant_user, reference_user)
     cur.execute(query)
     result =cur.fetchall()
     if cur.rowcount == 0:
        return ("None")
     else:
        return str(result)

# Translates the X and Y chromosomes into a chromosome number used to fetch data out of the database.
def chromo_dict(chromosome):
        chromosome_dict = {X:23,
                          Y:24}
        return chromosome_dict[chromosome.upper]

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')



