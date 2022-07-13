from db.dao import DAO
from leetcode_service.leetcode_client import LeetcodeClient

def populate_leetcode_questions():

    dao = DAO()
    num_questions = LeetcodeClient.GetNumQuestions()
    num_added = 0
    
    print("Verifying all problem entries are up to date with leetcode.com...")
    for i in range(1, num_questions+1):
        problem_query = str(i)
        
        question = dao.GetProblem(problem_query, n_args=1)

        if not question:
            try:
                question = LeetcodeClient.GetQuestionFromSearch(problem_query)
                dao.MakeProblem(question)
                num_added += 1
            except Exception as e:
                print(e)

        print(f"{i} of {num_questions} | {question.problem_name}")
    
    print(f"Added {num_added} new problems")

if __name__ == '__main__':
    populate_leetcode_questions()
