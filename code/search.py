import math

import sys
from github import Github
from github.GithubException import RateLimitExceededException, GithubException

from pymongo import MongoClient
import json
from datetime import date, timedelta, datetime
import time
from math import ceil

# Query the GitHub API to find jupyter notebooks. Collect the first 30 of them
# and write to a json file called data.json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

g = Github(data["git-user"], data["git-password"])
l =g.get_rate_limit()

client = MongoClient(data["mongo-host"], data["mongo-port"],
                     username=data["mongo-user"],
                     password=data["mongo-password"],
                     authSource=data["mongo-db"])

db = client[data["mongo-db"]]
collection = db["repositories"]


def retry_interval(retry_count):
    if retry_count < 3:
        return 30
    if retry_count < 10:
        return 90
    else:
        return 60 * 10

def safe_search(q):
    search_result = None
    retry_count = 0
    while not search_result:
        try:
            search_result = g.search_repositories(q)
            search_result.totalCount  # Force submission to API

        except RateLimitExceededException:
            search_result = None
            retry_count += 1
            interval = retry_interval(retry_count)
            print("Rate Limit Exceeded.... pausing %d seconds" % interval)
            time.sleep(interval)

        except GithubException:
            search_result = None
            retry_count += 1
            print("GitHub Server Error.... pausing for 15 minutes")
            time.sleep(60 * 15)

    return search_result

def safe_topics(repo):
    result = None
    retry_count = 0
    while result is None:
        try:
            result = repo.get_topics()

        except RateLimitExceededException:
            result = None
            retry_count += 1
            interval = retry_interval(retry_count)
            print("Topics Rate Limit Exceeded.... pausing %d seconds" % interval)
            time.sleep(interval)

        except GithubException:
            search_result = None
            retry_count += 1
            print("TopicRate GitHub Server Error.... pausing for 15 minutes")
            time.sleep(60 * 15)

    return result

def get_license(repo):
    reslt = None
    retry_count = 0

    while reslt is None:
        try:
            license = repo.get_license()
            reslt = {
                "license_key": license.license.key,
                "license": license.license.name
            }
        except RateLimitExceededException:
            result = None
            retry_count += 1
            interval = retry_interval(retry_count)
            print(
                "Licence Rate Limit Exceeded.... pausing %d seconds" % interval)
            time.sleep(interval)

        # except GithubException:
        #     search_result = None
        #     retry_count += 1
        #     print("Licence GitHub Server Error.... pausing for 15 minutes")
        #     time.sleep(60 * 15)
        except:
            reslt = {}

    return reslt


search_end = date.today()
# period_start = date(2008, 1, 1)
period_start = date(2016, 1, 25)
while (period_start < search_end):
    # Initial window size. We will reduce this if we exceed search limit with
    # this net
    range_size = timedelta(days=30)

    search_succeded = False
    while not search_succeded:
        period_end = period_start + range_size
        search_result = safe_search(
            'language:"Jupyter Notebook" is:public created:%s..%s' % (
                period_start, period_end))
        if (search_result.totalCount < 1000):
            print("(%s) %s + %d: %s" %
                  (datetime.isoformat(datetime.now()),
                   period_start.isoformat(), range_size.days,
                   search_result.totalCount))
            search_succeded = True
        else:
            range_size = timedelta(math.ceil(range_size.days * 0.75))

    for repo in search_result:
        license = get_license(repo)
        topics = safe_topics(repo)

        rec = {
            "id": repo.id,
            "name": repo.name,
            "full_name": repo.full_name,
            "owner": repo.owner.login,
            "description": repo.description,
            "fork": repo.fork,
            "created_at": repo.created_at,
            "homepage": repo.homepage,
            "stargazers_count": repo.stargazers_count,
            "watchers_count": repo.watchers_count,
            "license": license,
            "forks": repo.forks,
            "topics": topics
        }

        collection.insert(rec)
    period_start = period_end

search_result = g.search_repositories('language:"Jupyter Notebook" is:public')
# search_result = g.search_code("ipynb", extension="ipynb")
print(search_result.totalCount)
print(search_result.incomplete_results)

for content_file in search_result:
    print(content_file)
    # with urllib.request.urlopen(content_file.download_url) as url:
    #     notebook = json.loads(url.read().decode('utf-8-sig'))
    #
    # foo = {"repository": content_file.repository.full_name,
    #        "path": content_file.path,
    #        "sha": content_file.sha,
    #        "notebook": notebook}
    #
    # print(foo)
    # collection.insert(foo)
