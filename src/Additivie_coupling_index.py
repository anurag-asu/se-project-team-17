from pydriller import Repository
import json
import requests

# def get_contributors():
#     collaborators_url = "https://api.github.com/repos/leeoniya/uPlot/collaborators?affiliation=outside" 
#     response = requests.get(collaborators_url)

#     json_object= json.dump(response.json(), indent=4)

#     with open('collaborators.json','w') as outfile:
#         outfile.write



url = "https://github.com/spring-projects/spring-framework"
local_path = "./spring-framework"
repo = Repository(local_path)
commits = repo.traverse_commits()
first_commit = next(commits)
count = 0

for commit in commits:
    count+=1
    added = 0
    for m in commit.modified_files:
        if (m.change_type.name == "ADD"):
            added += 1

    files_changed = commit.files
    if(files_changed):
        additive_contribution = added/files_changed
        print(additive_contribution)