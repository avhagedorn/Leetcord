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

    QUESTION_OF_TODAY_QUERY = """
        query questionOfToday {
            activeDailyCodingChallengeQuestion {
                question {
                    frontendQuestionId: questionFrontendId
                    isPaidOnly
                    title
                    titleSlug
                    difficulty
                }
            }
        }    
    """

    QUESTION_OF_TODAY_OPERATION = "questionOfToday"

    PROBLEMS_PATH = "https://leetcode.com/problems"

    GRAPHQL_PATH = "https://leetcode.com/graphql"

    REST_PATH = "https://leetcode.com/api/problems/all/"
