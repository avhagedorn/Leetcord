from exceptions import NoMatchingQuestions, MalformedResponse, RequestFailed
from db.db_utils import standardize_difficulty
from db.models import Problem
from leetcode_service.leetcode_util import MakeGraphqlQuery, ParseSlugFromUrl
from leetcode_service.graphql_query_builder import GraphqlQueryBuilder

class LeetcodeClient:

    @staticmethod
    def GetQuestionFromSlug(slug: str) -> Problem:
        body = GraphqlQueryBuilder.BuildSlugQuery(slug)
        response = MakeGraphqlQuery(body)

        if response.ok:
            response = response.json()
            if 'data' in response and 'question' in response['data']:
                question = response['data']['question']
                return LeetcodeClient._BuildProblem(question)
            else:
                raise MalformedResponse()
        else:
            raise RequestFailed(response.text)

    @staticmethod
    def GetQuestionFromSearch(query: str) -> Problem:
        if query.startswith("https"):
            query = ParseSlugFromUrl(query)

        body = GraphqlQueryBuilder.BuildSearchQuery(query)
        response = MakeGraphqlQuery(body)

        if response.ok:
            response = response.json()
            if 'data' in response \
                and 'problemsetQuestionList' in response['data'] \
                and 'questions' in response['data']['problemsetQuestionList']:

                questions = response['data']['problemsetQuestionList']['questions']

                for question in questions:
                    if question['title'].lower() == query.lower() \
                        or question['titleSlug'].lower() == query.lower() \
                        or question['frontendQuestionId'] == query:
                        
                        return LeetcodeClient._BuildProblem(question)
                
                raise NoMatchingQuestions()
            else:
                raise MalformedResponse()
        else:
            raise RequestFailed(response.text)

    @staticmethod
    def GetNumQuestions() -> int:
        body = GraphqlQueryBuilder.BuildSearchQuery(query='', limit=1)
        response = MakeGraphqlQuery(body)

        if response.ok:
            response = response.json()
            if 'data' in response \
                and 'problemsetQuestionList' in response['data']:

                return response['data']['problemsetQuestionList']['totalNum']

            else:
                raise MalformedResponse()
        else:
            raise RequestFailed(response.text)

    @staticmethod
    def GetQuestionOfToday() -> Problem:
        body = GraphqlQueryBuilder.BuildQuestionOfTodayQuery()
        response = MakeGraphqlQuery(body)

        if response.ok:
            response = response.json()

            if 'data' in response \
                and 'activeDailyCodingChallengeQuestion' in response['data'] \
                and 'question' in response['data']['activeDailyCodingChallengeQuestion']:

                question = response['data']['activeDailyCodingChallengeQuestion']['question']
                return LeetcodeClient._BuildProblem(question)
            
            else:
                raise MalformedResponse()
        else:
            raise RequestFailed(response.text)

    @staticmethod
    def _BuildProblem(response) -> Problem:
        problem = Problem()

        try:
            problem.slug = response['titleSlug']
            problem.problem_name = response['title']
            problem.premium = response['isPaidOnly']
            problem.problem_number = response['frontendQuestionId']
            problem.difficulty = standardize_difficulty(response['difficulty'])

            return problem

        except KeyError:
            raise MalformedResponse()
