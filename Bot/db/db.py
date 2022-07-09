from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_constants import Constants
from models import Base, Member


engine = create_engine(Constants.CONNECTION_URL)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()

members = session.query(Member).all()
for member in members:
    print(member.discordName)

print(Base.metadata.tables.keys())

session.close()
