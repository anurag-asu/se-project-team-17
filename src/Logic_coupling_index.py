from pydriller import Repository
import pandas as pd
from github import Github


def get_repos():
    df = pd.read_csv("./metrics_combined - asfi_refined_with_metrics.csv")
    project_list = []
    project_list = df.corrected_pj_github_url
    print("No. of projects:", len(project_list))
    return project_list


def get_pairs(list):
    pairs = []
    for i in range(len(list)):
        for j in range(len(list)):
            pairs.append([list[i], list[j]])
    return pairs


# commit_files = [1,2,3,4]
# get_pairs(commit_files)


def logic_coupling_index():
    df = pd.read_csv("./metrics_combined - asfi_refined_with_metrics.csv")
    # df['logic_coupling_index'] = "NaN"
    repos = get_repos()
    # repo="https://github.com/apache/incubator-retired-amaterasu"
    i = 1
    for repo in repos:

        try:
            calculated = float(
                df.loc[df["corrected_pj_github_url"] == repo, "logic_coupling_index"]
            )
            if calculated > 0.0:
                continue
            r = Repository(repo, order="reverse")
            commits = r.traverse_commits()
            index = 0
            all_files = set()
            commit_files_list = []
            for commit in commits:
                index += 1
                commit_files = []

                # print(commit.committer_date)

                for m in commit.modified_files:
                    if m.change_type.name == "ADD" or m.change_type.name == "MODIFY":
                        all_files.add(m.filename)
                        commit_files.append(m.filename)

                if len(commit_files) > 1:
                    commit_files_list.append(commit_files)

                if index > 150:
                    # print(index)
                    break

            # print(all_files)

            index = 0
            modularity = []
            # print('----------------------')
            for commit_files in commit_files_list:
                # print(commit.committer_date)
                # commit_files=[]
                # for m in commit.modified_files:
                #     if (m.change_type.name == "ADD" or m.change_type.name == "MODIFY"):
                #         commit_files.append(m.filename)

                # commit_files = [1,2,3,4]   [[1,2],[1,3],[1,4],[2,3]...]

                if len(commit_files) > 1:
                    file_pairs = get_pairs(commit_files)
                    l = len(all_files)
                    list_all_files = list(all_files)
                    support_matrix = [[0 for x in range(l)] for y in range(l)]

                    for pairs in file_pairs:
                        a = list_all_files.index(pairs[0])
                        b = list_all_files.index(pairs[1])
                        support_matrix[a][b] += 1
                    # print(support_matrix)

                    count_bigger_than_zero = 0
                    for x in range(l):
                        for y in range(l):
                            if support_matrix[x][y] > 0:
                                count_bigger_than_zero += 1

                    # print(count_bigger_than_zero, l*l)
                    modularity_commit = count_bigger_than_zero / (l * l)
                    print(modularity_commit)

                    modularity.append(modularity_commit)

                #     commit_files_list.append(commit_files)
                # print(commit_files_list)
                # for idx in commit_files_list:
                #     print(idx)
                #     #     get_pairs(idx)

                index += 1
                if index > 150:
                    # print(index)
                    break

            logic_coupling_index = sum(modularity) / len(modularity)
            # print("logic",logic_coupling_index)
            df.loc[
                df["corrected_pj_github_url"] == repo, "logic_coupling_index"
            ] = logic_coupling_index
            print(i, repo, logic_coupling_index)
            i += 1
            df.to_csv("./metrics_combined - asfi_refined_with_metrics.csv", index=False)

        except Exception as e:
            print("Repo Failed:", repo)
            print("1,{}".format(e))
            # continue


logic_coupling_index()


# all_files=['a', 'b', 'c', 'd', 'e', 'f']

# commit_files=["b","d","f"]

# file_pairs = get_pairs(commit_files)
# print(file_pairs)
# l = len(all_files)
# list_all_files = list(all_files)
# support_matrix = [[0 for x in range(l)] for y in range(l)]

# for pairs in file_pairs:
#     a = list_all_files.index(pairs[0])
#     b = list_all_files.index(pairs[1])
#     support_matrix[a][b] = 1

# for x in range(l):
#     for y in range(l):
#         print(support_matrix[x][y], end=' ')
#     print(' ')
