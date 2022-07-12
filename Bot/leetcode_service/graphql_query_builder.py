from leetcode_service.leetcode_constants import Constants

class GraphqlQueryBuilder:

    @staticmethod
    def BuildSlugQuery(slug):
        return GraphqlQueryBuilder._BuildQuery(
            query=Constants.QUESTION_QUERY,
            operationName=Constants.QUESTION_OPERATION,
            variables= {
                'titleSlug' : slug
            }
        )
    
    @staticmethod
    def BuildSearchQuery(query, limit=5):
        return GraphqlQueryBuilder._BuildQuery(
            query=Constants.PROBLEMSET_QUERY,
            operationName=Constants.PROBLEMSET_OPERATION,
            variables={
                'categorySlug' : '',
                'limit' : limit,
                'filters' : {
                    'searchKeywords' : query
                }
            }
        )

    @staticmethod
    def BuildQuestionOfTodayQuery():
        return GraphqlQueryBuilder._BuildQuery(
            query=Constants.QUESTION_OF_TODAY_QUERY,
            operationName=Constants.QUESTION_OF_TODAY_OPERATION,
            variables=None
        )

    @staticmethod
    def _BuildQuery(query, operationName, variables):
        return {
            'query' : query,
            'operationName' : operationName,
            'variables' : variables
        }