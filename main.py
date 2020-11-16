import requests
import json
import pprint

def compareN(x): #sort in descending order on the basis of forks_count
    return -x['forks_count']

def compareM(x):  #sort in descending order on the basis of contributions
    return -x['contributions']

def isOrgExist(orgname):
    url = "https://api.github.com/orgs/" + orgname
    res = requests.get(url)
    res = res.content
    res = json.loads(res)
    try:
        if res['message'] == "Not Found":
            return False
        return True
    except:
        return True


def getTopNRepos(orgname , n):
    url = "https://api.github.com/orgs/" + orgname + "/repos"
    res = requests.get(url)
    res = json.loads(res.content)


    res = sorted(res , key = compareN)

    topNRepos = []
    for i in range(min(n , len(res))):
        topNRepos.append(res[i]["name"])

    return topNRepos

def getTopMCommitee(orgname , reponame , m):
    url = "https://api.github.com/repos/" + orgname + "/" + reponame + "/contributors"
    res = requests.get(url)
    res = json.loads(res.content)

    res = sorted(res , key = compareM)

    data = {}
    topMCommitee = []
    data["reponame"] = reponame
    for i in range(min(m , len(res))):
        map = {}
        map["username"] = res[i]['login']
        map["commit_count"] = res[i]['contributions']
        topMCommitee.append(map)

    data["contributions"] = topMCommitee

    return data

if __name__ == '__main__':
    orgname = input()
    n = int(input())
    m = int(input())

    if isOrgExist(orgname) == False :  #If organisation name does not exists
        print("Organization does not exists!!")

    topN = getTopNRepos(orgname , n)

    result = []
    for i in topN:
        data = getTopMCommitee(orgname , i , m)
        result.append(data)

    print(json.dumps(result , indent=4))