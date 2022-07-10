from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import sessionmaker
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
        return self._session.execute(query).scalars().first()



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
