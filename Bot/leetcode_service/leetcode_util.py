import requests
from leetcode_service.leetcode_constants import Constants

def MakeGraphqlQuery(body: str):
    return requests.post(url=Constants.GRAPHQL_PATH, json=body)

def ParseSlugFromUrl(url: str):
    parts = url.split('/')
    try:
        i = parts.index('problems') + 1
        return parts[i]
    except:
        raise Exception("Invalid URL")

