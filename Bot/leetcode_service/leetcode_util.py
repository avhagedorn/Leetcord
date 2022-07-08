import requests
from leetcode_service.leetcode_constants import Constants

def MakeGraphqlQuery(body: str):
    return requests.post(url=Constants.GRAPHQL_PATH, json=body)

def ParseSlugFromUrl(url: str):
    PATH_LENGTH = len(Constants.PROBLEMSET) + 1

    if len(url) > PATH_LENGTH:
        url = url.rstrip('/')
        return url[PATH_LENGTH:]
    
    raise Exception("Invalid URL")
