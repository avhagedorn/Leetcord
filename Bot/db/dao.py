from typing import List
from sqlalchemy import create_engine, select
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker, subqueryload
from datetime import datetime
from leetcode_service.leetcode_util import ParseSlugFromUrl
from db.models import Problem, Solve
from db.db_constants import Constants
from db.models import Base, Member

class DAO:
    _instance = None

    def MakeMember(self, member: Member):
        self._session.add(member)
        self._session.commit()

        return member

    def MakeProblem(self, problem: Problem):
        self._session.add(problem)
        self._session.commit()

        return problem

    def Solved(self, solvee: Member, problem: Problem):
        solution = Solve()
        solution.date = datetime.now()
        solution.problem = problem
        solution.solvee = solvee
        solution.takeaway = ''
        
        solvee.num_solutions += 1
        self._session.add(solvee)
        self._session.add(solution)
        self._session.commit()

        return solution

    def UpdateTakeaway(self, solution: Solve, takeaway: str):
        solution.takeaway = takeaway
        self._session.add(solution)
        self._session.commit()

        return solution

    def DeleteSolution(self, solution):
        solvee = solution.solvee
        solvee.num_solutions -= 1
        self._session.add(solvee)
        self.DeleteRow(solution)

    def DeleteRow(self, obj):
        klass = obj.__class__

        if klass in Constants.MODELS:
            self._session.delete(obj)
            self._session.commit()
            
        else:
            raise Exception(
                f"""
                Given row is not a member of the models: {
                    [klass.__name__ for klass in Constants.MODELS]
                }    
                """
            )

    def GetMember(self, discordID: str) -> Member:
        query = select(Member).where(Member.discordID == discordID)
        return self._FindFirst(query)

    def GetMemberStats(self, member: Member):
        joins = self._session.query(Solve).join(Solve.problem).where(Solve.solvee == member)
        retVal = [0, 0, 0]

        for k in Constants.DIFFICULTY_MAPPING.keys():
            retVal[k] = joins.where(Problem.difficulty == k).count()

        return retVal

    def GetTopUsers(self, limit: int = 10):
        return self._session.query(Member).order_by(Member.num_solutions.desc()).limit(limit).all()

    def GetSolution(self, id: int) -> Solve:
        query = select(Solve).where(Solve.id == id)
        return self._FindFirst(query)
    
    def GetProblem(self, search: str, n_args: int) -> Problem:

        if search.isnumeric():
            # Query based on problem number
            problem_number = int(search)
            return self._GetProblemByNumber(problem_number)

        elif search.startswith('https'):
            # Query based on slug
            slug = ParseSlugFromUrl(search)
            return self._GetProblemBySlug(slug)

        elif n_args == 1:
            # Query based on slug
            return self._GetProblemBySlug(search)

        else:
            # Query based on title
            return self._GetProblemByTitle(search)

    def RecentProblemSolutions(self, problem: Problem = None, limit: int = 5) -> List[Solve]:
        query = select(Solve)
        if problem:
            query = query.where(Solve.problem == problem)
        query = query.order_by(Solve.date.desc()).limit(limit).options(subqueryload(Solve.solvee))
        return self._session.execute(query).scalars().all()

    def RecentUserSolutions(self, solvee: Member = None, limit: int = 5) -> List[Solve]:
        query = select(Solve)
        if solvee:
            query = query.where(Solve.solvee == solvee)
        query = query.order_by(Solve.date.desc()).limit(limit).options(subqueryload(Solve.problem))
        return self._session.execute(query).scalars().all()

    def GetRandomProblem(self, difficulty_filter, includes_premium) -> Problem:
        # query = select(Problem).where(Problem.premium == includes_premium)
        # if difficulty_filter is not None:
        #     query = query.where(Problem.difficulty == difficulty_filter)
        query = self._session.query(Problem).order_by(func.random()).all()
        print([str(t) for t in query])
        return query #.first() # self._FindFirst(query)

    def _GetProblemByNumber(self, number: int):
        query = select(Problem).where(Problem.problem_number == number)
        return self._FindFirst(query)
    
    def _GetProblemBySlug(self, slug: str):
        query = select(Problem).where(Problem.slug == slug)
        return self._FindFirst(query)
    
    def _GetProblemByTitle(self, title: str):
        query = select(Problem).where(Problem.problem_name == title)
        return self._FindFirst(query)

    def _FindFirst(self, query):
        return self._session.execute(query.limit(1)).scalars().first()

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
