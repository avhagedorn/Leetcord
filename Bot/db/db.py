import os
import json
import pyodbc

if os.path.exists(os.path.join(os.path.dirname(__file__),"config.json")):
    f = open(os.path.join(os.path.dirname(__file__),"config.json"))
    data = json.load(f)
    f.close()

def load(key):
    return os.getenv(key) or data[key]

conn_str = 'Driver={ODBC Driver 17 for SQL Server};SERVER='+load("DBHOST")+',1433;DATABASE='+load("DBNAME")+';UID='+load("DBUSER")+';PWD='+load("DBPASS")
print(conn_str)
engine_azure = pyodbc.connect(conn_str)

connection = engine_azure.cursor()

connection.execute("SELECT * FROM data_member")
row = connection.fetchone()

print(row)


print("hi")