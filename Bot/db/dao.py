from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from db.db_constants import Constants
from db.models import Base, Member

class DAO:
    _instance = None

    def GetMember(self, discordID: str):
        query = select(Member).where(Member.discordID == discordID)
        return self._session.execute(query).scalars().first()

    def MakeMember(self, member: Member):
        self._session.add(member)
        self._session.commit()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DAO, cls).__new__(cls)
            
            engine = create_engine(Constants.CONNECTION_URL)            
            Base.metadata.create_all(bind=engine)
            Session = sessionmaker(bind=engine)
            cls._session = Session()

        return cls._instance

    def __del__(cls):
        cls._session.close()
