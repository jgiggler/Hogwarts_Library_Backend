from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_gilgerj'
app.config['MYSQL_PASSWORD'] = 'BwnvI38JjlR6' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_gilgerj'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    

    query4 = 'SELECT * FROM Books;';
    cur = mysql.connection.cursor()
    cur.execute(query4)
    results = cur.fetchall()

    return "<h1>MySQL Results</h1>" + str(results[0])


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=4545, debug=True)