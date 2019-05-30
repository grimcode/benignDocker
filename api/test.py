from flask import Flask, render_template
import pymysql
app = Flask(__name__)
host = "172.17.0.2"
user = "benignDB"
password = "docker"
db = "benignDB"
con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                           DictCursor)
cur = con.cursor()
