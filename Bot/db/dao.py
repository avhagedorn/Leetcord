from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from leetcode_service.leetcode_util import ParseSlugFromUrl
from db.models import Problem, Solve
from db.db_constants import Constants
from db.models import Base, Member

class DAO:
    _instance = None

    def MakeMember(self, member: Member):
        self._session.add(member)
        self._session.commit()

    def MakeProblem(self, problem: Problem):
        self._session.add(problem)
        self._session.commit()

    def Solve(self, solve: Solve):
        self._session.add(solve)
        self._session.commit()



    def GetMember(self, discordID: str):
        query = select(Member).where(Member.discordID == discordID)
        return self._FindFirst(query)
    
    def GetProblem(self, search: str, n_args: int):

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
