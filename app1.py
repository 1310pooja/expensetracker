from flask import Flask, jsonify
import mysql.connector
from mysql.connector import errorcode
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            database=app.config['MYSQL_DATABASE'],
           # ssl_ca=app.config['MYSQL_SSL_CA'],
            ssl_disabled=app.config['MYSQL_SSL_DISABLED'],
           
        )
        print(conn)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"Database": db_name[0]})
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

if __name__ == '__main__':
    app.run(debug=True)
