import os
import json
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date, SmallInteger, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.engine import URL

Base = declarative_base()

class Member(Base):
    __tablename__ = "data_member"

    id = Column(Integer, primary_key=True)
    discordID = Column('discordID', Integer)
    discordName = Column('discordName', VARCHAR(35))
    discordPFP = Column('discordPFP', String)
    date_verified = Column('date_verified', Date)

class Problem(Base):
    __tablename__ = "data_problem"

    id = Column(Integer, primary_key=True)
    problem_number = Column('problem_number', SmallInteger, primary_key=True)
    slug = Column('slug', VARCHAR(200))
    difficulty = Column('difficulty', SmallInteger)

    solutions = relationship('Solve', back_populates='problem')

class Solve(Base):
    __tablename__ = "data_solve"

    id = Column(Integer, primary_key=True)

    solvee_id = Column(Integer, ForeignKey('member.id', ondelete='CASCADE'))
    solvee = relationship('Member', back_populates='solutions')

    date = Column('date', Date)

    problem_id = Column(Integer, ForeignKey('problem.id', ondelete='CASCADE'))
    problem = relationship('Problem', back_populates='solutions')

    takeaway = Column('takeaway', VARCHAR(255))

