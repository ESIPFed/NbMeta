import base64
import json
from datetime import datetime
import time

import math

from github import Github, RateLimitExceededException, GithubException
from pymongo import MongoClient

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

g = Github(data["git-user"], data["git-password"])
# Keep track of this for throttleing
total_notebooks = 0

client = MongoClient(data["mongo-host"], data["mongo-port"],
                     username=data["mongo-user"],
                     password=data["mongo-password"],
                     authSource=data["mongo-db"])

db = client[data["mongo-db"]]
repo_collection = db["repositories"]
notebook_collection = db["notebooks"]

def retry_interval(retry_count):
    if retry_count < 3:
        return 30
    if retry_count < 10:
        return 90
    else:
        return 60 * 10

def throttle_api():
    global total_notebooks
    total_notebooks += 1
    if(total_notebooks % 175 == 0):
        print("...pause...")
        time.sleep(60)

def get_repo(collection):
    cursor = collection.find({"notebook_count": {"$exists": False}})

    ## Avoid timeouts in the cursor while we load a repo full of notebooks
    cursor.batch_size(5)
    for repo in cursor:
        yield repo

def get_notebook(repo):
    retry_count = 0
    try:
        search_result = g.search_code("repo:%s extension:ipynb" % repo['full_name'])
        for notebook in search_result:
            throttle_api()
            yield notebook

    except RateLimitExceededException:
        search_result = None
        retry_count += 1
        interval = retry_interval(retry_count)
        print("Rate Limit Exceeded.... pausing %d seconds" % interval)
        time.sleep(interval)

    except GithubException as e:
        print("Received an exception while reading notebooks "+str(e))



def download_notebook(content_file):
    repo = content_file.repository
    blob = repo.get_git_blob(content_file.sha)
    if math.floor(blob.size / 1e6) < 16:
        content = base64.b64decode(blob.content).decode('utf-8-sig')
        try:
            return json.loads(content)
        except json.decoder.JSONDecodeError:
            print("hhmmm "+str(content))
            return {
            "cells":[],
            "metadata": {
                "file_truncated":True,
                "file_size": blob.size,
                "file_download_error":True
            }
        }
    else:
        return {
            "cells":[],
            "metadata": {
                "file_truncated":True,
                "file_size": blob.size
            }
        }


def generate_db_record(content_file):
    notebook = download_notebook(content_file)

    return {"repository": content_file.repository.full_name,
                "path": content_file.path,
                "sha": content_file.sha,
                "notebook": notebook}

for r in get_repo(repo_collection):
    print(r)
    notebook_count = 0
    for content_file in get_notebook(r):
        notebook_rec = generate_db_record(content_file)

        notebook_collection.insert(notebook_rec, check_keys=False)
        print("%s --> %s" %(datetime.isoformat(datetime.now()), content_file.path))
        notebook_count += 1

    print("Processed %d notebooks in repo %s" % (notebook_count, r['full_name']))
    repo_collection.update_one({"_id": r['_id']},
                               {"$set":
                                   {
                                   "notebook_count": notebook_count
                                   }
                               })


print("Done with all repos")