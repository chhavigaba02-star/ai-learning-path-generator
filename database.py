import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Chhavi3124",
        database="learning",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def test_connection():
    try:
        conn = get_connection()
        conn.close()
        print("Database connected successfully")
    except Exception as e:
        print("Oh No!Database connection failed:", e)
