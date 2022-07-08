class Constants:

    LEETCODE_QUERY = """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                titleSlug
                difficulty
            }
        }
    """

    OPERATION_NAME = "questionData"

    PROBLEMS_PATH = "https://leetcode.com/problems"

    GRAPHQL_PATH = "https://leetcode.com/graphql"
