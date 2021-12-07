from pydriller import Repository
import pandas as pd
from github import Github

# Generate a token at https://github.com/settings/tokens
# token = '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'

# g = Github(token)

# repo_name = 'spring-projects/spring-framework'
# repo = g.get_repo(repo_name)
# collaborators = repo.get_collaborators()

# for collaborator in collaborators:
#     print (collaborator.login)


def get_repos():
	df = pd.read_csv("./asfi_refined_false_removed.csv") 
	project_list = []
	project_list = df.corrected_pj_github_url
	print("No. of projects:", len(project_list))
	return project_list

def Additive_contributing_index():
    df = pd.read_csv("./asfi_refined_false_removed.csv")  
    # df['additive_contribution_index'] = "NaN"
    repos = get_repos()
    count = 0
    for repo in repos:
        try:
            # calculated = float(df.loc[df['corrected_pj_github_url'] == repo, 'additive_contribution_index'])
            # if calculated > 0.0:
            #     continue
            
            r = Repository(repo)
            commits = r.traverse_commits()
            additive_contribution = 0
            for commit in commits:
                count+=1
                added = 0
                for m in commit.modified_files:
                    if (m.change_type.name == "ADD"):
                        added += 1

                files_changed = commit.files
                if(files_changed):
                    additive_contribution += added/files_changed
                    # print(added/files_changed)

            additive_contribution_index = additive_contribution / count
            count = 0
            df.loc[df['corrected_pj_github_url'] == repo, 'additive_contribution_index'] = additive_contribution_index
            print(repo,additive_contribution_index)
            df.to_csv("./asfi_refined_false_removed.csv", index=False)
        except Exception as e: 
            print("Repo Failed:", repo)
            print('{}'.format(e))
            pass

Additive_contributing_index()