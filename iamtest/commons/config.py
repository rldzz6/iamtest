import sys
import os
import pydapper
import pymysql
import mysql.connector

def db_connection():
    try:
        DB_HOST='localhost'
        DB_USER='root'
        DB_PASSWORD=''
        DB_DATABASE='sys'
        conn = mysql.connector.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASSWORD,db=DB_DATABASE, port='3306', charset='utf8')
        commands =pydapper.using(conn)

        return commands
    except Exception as err_msg:
        raise('********ERROR********' + err_msg)