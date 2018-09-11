from github import Github
import json
import urllib.request

# Query the GitHub API to find jupyter notebooks. Collect the first 30 of them
# and write to a json file called data.json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

with open('data.json') as json_data_file:
    search_result = json.load(json_data_file)

g = Github(data["git-user"], data["git-password"])

print(len(search_result))

for content in search_result[0:3]:
    repo = g.get_repo(content["repository"], lazy=False)
    file = repo.get_file_contents(content["path"])
    commits = repo.get_commits(path=content["path"])
    print(repo)
    print(file.download_url)

    with urllib.request.urlopen(file.download_url) as url:
        data = json.loads(url.read().decode())
        print(data)


    for commit in commits:
        print("repo owner: %s  commiter: %s  author:%s "%(repo.owner, commit.committer, commit.author))
        if(repo.owner):
            print(str(repo.owner.name) + " "+str(repo.owner.login) + " "+ str(repo.owner.email))
    print("\n\n")
