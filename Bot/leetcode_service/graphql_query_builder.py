from leetcode_service.leetcode_constants import Constants

class GraphqlQueryBuilder:

    @staticmethod
    def BuildLeetcodeQuery(title_slug):
        return {
            'query' : Constants.LEETCODE_QUERY,
            'operationName' : Constants.OPERATION_NAME,
            'variables' : {
                'titleSlug' : title_slug
            }
        }