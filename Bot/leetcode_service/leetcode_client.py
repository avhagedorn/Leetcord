import requests
from leetcode_service.leetcode_constants import Constants
from leetcode_service.leetcode_question import LeetcodeQuestion
from leetcode_service.graphql_query_builder import GraphqlQueryBuilder

class LeetcodeClient:

    @staticmethod
    def GetQuestion(slug: str) -> LeetcodeQuestion:
        body = GraphqlQueryBuilder.BuildLeetcodeQuery(slug)
        response = requests.post(url=Constants.GRAPHQL_PATH, json=body)

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
