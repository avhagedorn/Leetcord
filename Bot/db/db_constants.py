import os
import json
import enum
from sqlalchemy.engine import URL

if os.path.exists(os.path.join(os.path.dirname(__file__),"config.json")):
    f = open(os.path.join(os.path.dirname(__file__),"config.json"))
    data = json.load(f)
    f.close()

def load(key):
    return os.getenv(key) or data[key]


class Constants:

    CONNECTION_STRING = 'Driver={ODBC Driver 17 for SQL Server}'+ \
                        ';SERVER='+load("DBHOST")+',1433' + \
                        ';DATABASE='+load("DBNAME")+ \
                        ';UID='+load("DBUSER")+ \
                        ';PWD='+load("DBPASS")

    CONNECTION_URL = URL.create(
                        "mssql+pyodbc", 
                        query={"odbc_connect": CONNECTION_STRING}
                    )

