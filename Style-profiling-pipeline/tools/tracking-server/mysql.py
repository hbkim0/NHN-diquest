import sys
import pymysql 

import config


_DATABASE_NAME = 'mamihlapinatapai'


mysql_db = pymysql.connect(
    user=config.DATABASE['tracking-server']['user'],
    passwd=config.DATABASE['tracking-server']['passwd'],
    host=config.DATABASE['tracking-server']['host'],
)

cursor = mysql_db.cursor()

if sys.argv[1] == "clean":    
    sql = f"DROP database {_DATABASE_NAME};"
    cursor.execute(sql)
    print("remove database: mamihlapinatapai")
    
elif sys.argv[1] == "create":
    sql = f"create database {_DATABASE_NAME};"
    cursor.execute(sql)
    print("create database: mamihlapinatapai")