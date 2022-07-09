import os
import json
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

if os.path.exists(os.path.join(os.path.dirname(__file__),"config.json")):
    f = open(os.path.join(os.path.dirname(__file__),"config.json"))
    data = json.load(f)
    f.close()

def load(key):
    return os.getenv(key) or data[key]

connection_string = 'Driver={ODBC Driver 17 for SQL Server};SERVER='+load("DBHOST")+',1433;DATABASE='+load("DBNAME")+';UID='+load("DBUSER")+';PWD='+load("DBPASS")
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = create_engine(connection_url)
