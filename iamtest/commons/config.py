import sys
import os
import pydapper
import pymysql
import mysql.connector
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def db_connection():
    try:
        DB_HOST='localhost'
        DB_USER='root'
        DB_PASSWORD=''
        DB_DATABASE='sys'
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_DATABASE, connect_timeout=5)
        #conn = mysql.connector.connect(host=os.environ.get('DB_HOST'), user=os.environ.get('DB_USER'), passwd=os.environ.get('DB_PASSWORD'), db=os.environ.get('DB_DATABASE'), charset='utf8')

        return conn
    except Exception as error:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(error)
        sys.exit(1)
