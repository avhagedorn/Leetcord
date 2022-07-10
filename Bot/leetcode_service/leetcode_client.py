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

                problem = Problem()
                problem.problem_number = question
                problem.problem_name = question['title']
                problem.difficulty = standardize_difficulty(question['difficulty'])
                problem.premium = question['isPaidOnly']
                problem.slug = slug

                return problem
            else:
                raise Exception()
        else:
            raise Exception(response.text)

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
                        
                        problem = Problem()
                        problem.problem_number = question['frontendQuestionId']
                        problem.problem_name = question['title']
                        problem.difficulty = standardize_difficulty(question['difficulty'])
                        problem.slug = question['titleSlug']
                        problem.premium = question['isPaidOnly']

                        return problem
                
                raise Exception("No questions matched")
            else:
                raise Exception("Malformed response")
        else:
            raise Exception(response.text)
