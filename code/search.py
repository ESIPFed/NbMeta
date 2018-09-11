from github import Github
import json

# Query the GitHub API to find jupyter notebooks. Collect the first 30 of them
# and write to a json file called data.json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

g = Github(data["git-user"], data["git-password"])

search_result = g.search_code("ipynb", extension="ipynb")
print(search_result.totalCount)

save_list = list(map(lambda content_file:
                     {"repository":content_file.repository.full_name,
                      "path": content_file.path}, search_result[0:30]))

with open('data.json', 'w') as outfile:
    json.dump(save_list, outfile)

