from leetcode_service.leetcode_util import MakeGraphqlQuery, ParseSlugFromUrl
from leetcode_service.leetcode_question import LeetcodeQuestion
from leetcode_service.graphql_query_builder import GraphqlQueryBuilder

class LeetcodeClient:

    @staticmethod
    def GetQuestionFromSlug(slug: str) -> LeetcodeQuestion:
        body = GraphqlQueryBuilder.BuildSlugQuery(slug)
        response = MakeGraphqlQuery(body)

        if response.ok:
            response = response.json()
            if 'data' in response and 'question' in response['data']:
                response_question = response['data']['question']
                print(response_question)
                return LeetcodeQuestion(
                    slug = slug,
                    title = response_question['title'],
                    difficulty = response_question['difficulty'],
                )
            else:
                raise Exception()
        else:
            raise Exception(response.text)

    @staticmethod
    def GetQuestionFromSearch(query: str) -> LeetcodeQuestion:
        if query.startswith("https"):
            query = ParseSlugFromUrl(query)

        body = GraphqlQueryBuilder.BuildSearchQuery(query)
        response = MakeGraphqlQuery(body)

        if response.ok:
            response = response.json()
            if 'data' in response and 'problemsetQuestionList' in response['data']:
                questions = response['data']['problemsetQuestionList']['questions']

                for question in questions:
                    if question['title'] == query \
                        or question['titleSlug'] == query \
                        or question['frontendQuestionId'] == query:
                        
                        return LeetcodeQuestion(
                            slug=question['titleSlug'],
                            title=question['title'],
                            difficulty=question['difficulty']
                        )
                
                raise Exception("No questions matched")
            else:
                raise Exception()
        else:
            raise Exception(response.text)