from github import Github
import json
from pymongo import MongoClient
import json
import urllib.request

# Query the GitHub API to find jupyter notebooks. Collect the first 30 of them
# and write to a json file called data.json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

g = Github(data["git-user"], data["git-password"])

client = MongoClient(data["mongo-host"], data["mongo-port"],
                     username=data["mongo-user"],
                     password=data["mongo-password"],
                     authSource=data["mongo-db"])

db = client[data["mongo-db"]]
collection = db["notebooks"]

search_result = g.search_code("ipynb", extension="ipynb")
print(search_result.totalCount)

for content_file in search_result[0:50]:
    with urllib.request.urlopen(content_file.download_url) as url:
        notebook = json.loads(url.read().decode('utf-8-sig'))

    foo = {"repository": content_file.repository.full_name,
           "path": content_file.path,
           "sha": content_file.sha,
           "notebook": notebook}

    collection.insert(foo)
