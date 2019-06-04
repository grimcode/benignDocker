#!/usr/local/bin/python3
from flask import Flask, render_template
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



@app.route('/<int:chromID_user>/<int:position_user>/<string:variant_user>')
def pathroute(chromID_user,position_user,variant_user):
    cur = con.cursor()
    query = "SELECT * FROM Mutations NATURAL JOIN Chromosomes WHERE Mutations.chromID = {} and Mutations.position ={} and variant = \"{}\"  and benign = 0".format(chromID_user,position_user,variant_user)
    cur.execute(query)
    return (cur.fetchall())


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')



