
from flask import Flask, request,jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

def db_connection():
    conn=None
    try:                
        conn = pymysql.connect(
        host='localhost',
        database='Ecom',
        user='root',
        password='1131',
        cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(e)
    return conn


if __name__=='__main__':
    app.run(debug=True)