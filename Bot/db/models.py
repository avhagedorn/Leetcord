from sqlalchemy import BOOLEAN, Column, String, Integer, ForeignKey, Date, SmallInteger, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from leetcode_service.leetcode_constants import Constants

Base = declarative_base()

class Member(Base):
    __tablename__ = "data_member"

    id = Column(Integer, primary_key=True)
    discordID = Column('discordID', Integer)
    discordName = Column('discordName', VARCHAR(35))
    discordPFP = Column('discordPFP', String)
    date_verified = Column('date_verified', Date)
    num_solutions = Column('num_solutions', Integer)

    solutions = relationship('Solve', back_populates='solvee')

    def __str__(self) -> str:
        return f"Member {self.discordName} verified on {self.date_verified}"


class Problem(Base):
    __tablename__ = "data_problem"

    id = Column(Integer, primary_key=True)
    problem_number = Column('problem_number', SmallInteger)
    problem_name = Column('problem_name', VARCHAR(200))
    slug = Column('slug', VARCHAR(200))
    difficulty = Column('difficulty', SmallInteger)
    premium = Column('premium', BOOLEAN)

    solutions = relationship('Solve', back_populates='problem')

    def _url(self) -> str:
        return f"{Constants.PROBLEMS_PATH}/{self.slug}"

    def __str__(self) -> str:
        return f"Leetcode {self.problem_number} : {self.slug} | {self.difficulty}"


class Solve(Base):
    __tablename__ = "data_solve"

    id = Column(Integer, primary_key=True)
    date = Column('date', Date)
    takeaway = Column('takeaway', VARCHAR(255))

    solvee_id = Column(Integer, ForeignKey('data_member.id', ondelete='CASCADE'))
    solvee = relationship('Member', back_populates='solutions')

    problem_id = Column(Integer, ForeignKey('data_problem.id', ondelete='CASCADE'))
    problem = relationship('Problem', back_populates='solutions')

    def _url(self) -> str:
        return f"{Constants.Leetcord.SOLUTION_PATH}/{self.id}"

    def __str__(self) -> str:
        return f"{self.solvee.discordName}'s solution to {self.problem} on {self.date}"
