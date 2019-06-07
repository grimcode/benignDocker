#!/usr/local/bin/python3
from flask import Flask, render_template,request
import pymysql
import os, getpass



print (getpass.getuser())
app = Flask(__name__)
host = "172.17.0.2"
user = "root"
password = "docker"
db = "benignDB"
con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                           DictCursor)

<<<<<<< HEAD


@app.route('/<int:chromID_user>/<int:position_user>/<string:variant_user>')
def pathroute(chromID_user,position_user,variant_user):
    cur = con.cursor()
    query = "SELECT * FROM Mutations NATURAL JOIN Chromosomes WHERE Mutations.chromID = {} and Mutations.position ={} and variant = \"{}\"  and benign = 0".format(chromID_user,position_user,variant_user)
    cur.execute(query)
    return (str(cur.fetchall()))

=======
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
        return ("Niet alle benodige argumenten zijn meegegeven")
     cur = con.cursor()
     if (cancer is None or  cancer == 'N' or  cancer == 'NO'):
        query = "SELECT * FROM Mutations NATURAL JOIN Chromosomes WHERE Mutations.chromID = {} and Mutations.position ={} and variant = \"{}\" and Mutations.REFERENCE = \"{}\"  and benign = 0".format(chromID_user,position_user,variant_user, reference_user)
     else:
        query = "SELECT * FROM Mutations NATURAL JOIN Chromosomes WHERE Mutations.chromID = {} and Mutations.position ={} and variant = \"{}\" and Mutations.REFERENCE = \"{}\"   and benign = 0 and cancerCount > 0".format(chromID_user,position_user,variant_user, reference_user)
     cur.execute(query)
     result =cur.fetchall()
     if cur.rowcount == 0:
        return ("Uw query heeft geen match gevonden in de database")
     else:
        return str(result)


def chromo_dict(chromosome):
        chromosome_dict = {X:23,
                          Y:24}
        return chromosome_dict[chromosome.upper]
>>>>>>> b1dce767c7321ba4639b67a80215f80d5894679b

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')



