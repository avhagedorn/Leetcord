import os
import json
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from db_constants import Constants
from models import Base, Member

# if os.path.exists(os.path.join(os.path.dirname(__file__),"config.json")):
#     f = open(os.path.join(os.path.dirname(__file__),"config.json"))
#     data = json.load(f)
#     f.close()

# def load(key):
#     return os.getenv(key) or data[key]

# connection_string = 'Driver={ODBC Driver 17 for SQL Server};SERVER='+load("DBHOST")+',1433;DATABASE='+load("DBNAME")+';UID='+load("DBUSER")+';PWD='+load("DBPASS")
# connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

# connection = pyodbc.connect(connection_string)

# cursor = connection.cursor()

# for row in cursor.columns(table='DATA_SOLVE'):
#     print(row.column_name)

engine = create_engine(Constants.CONNECTION_URL)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

members = session.query(Member).all()
for member in members:
    print(member)
    print([str(s) for s in member.solutions])

print(Base.metadata.tables.keys())

session.close()
