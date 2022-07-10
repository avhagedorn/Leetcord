class Constants:

    QUESTION_QUERY = """
        query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                titleSlug
                difficulty
            }
        }
    """

    QUESTION_OPERATION = "questionData"

    PROBLEMSET_QUERY = """
        query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
            problemsetQuestionList: questionList(categorySlug: $categorySlug, limit: $limit, skip: $skip, filters: $filters) {
                totalNum
                questions: data {
                    acRate
                    difficulty
                    frontendQuestionId: questionFrontendId
                    title
                    titleSlug
                    isPaidOnly
                }
            }
        }
    """

    PROBLEMSET_OPERATION = "problemsetQuestionList"

    PROBLEMS_PATH = "https://leetcode.com/problems"

    GRAPHQL_PATH = "https://leetcode.com/graphql"
