from leetcode_service.leetcode_constants import Constants

class GraphqlQueryBuilder:

    @staticmethod
    def BuildSlugQuery(title_slug):
        return {
            'query' : Constants.QUESTION_QUERY,
            'operationName' : Constants.QUESTION_OPERATION,
            'variables' : {
                'titleSlug' : title_slug
            }
        }
    
    @staticmethod
    def BuildSearchQuery(query):
        return {
            'query' : Constants.PROBLEMSET_QUERY,
            'operationName' : Constants.PROBLEMSET_OPERATION,
            'variables' : {
                'categorySlug' : '',
                'filters' : {
                    'searchKeywords' : query
                }
            }
        }