from flask import Flask, render_template
import pymysql
import os, getpass



print (getpass.getuser())
app = Flask(__name__)
mysql.init_app(app)
host = "172.17.0.2"
user = "root"
password = "docker"
db = "benignDB"
con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                           DictCursor)

'''

@app.route('/pathroute/<path:mypath>/<int:chromID_user>/<int:position_user>/<string:variant_user>')
def pathroute(mypath,chromID_user,position_user,variant_user):
    #parsed = urlparse.urlparse(mypath)
   # print(urlparse.parse_qs(parsed.query)['def'])
   print (mypath)
'''
cur = con.cursor()
chromID_user = 21
position_user = 11085688
variant_user =  "C"
query = "SELECT * FROM Mutations NATURAL JOIN Chromosomes WHERE Mutations.chromID = {} and Mutations.position ={} and variant = {} and benign = 0".format(chromID_user,position_user,variant_user)
cur.execute(query)
print(cur.fetchall())

