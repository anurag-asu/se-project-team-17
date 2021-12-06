""" 
pre communication  index 

TODO:
    1. announcement of WIP ✅
    2. Auther is assigned in the PR ✅
    3. PR has issue (threat to validity if PR is tagged instead of issue) ✅
        1. Auther is assigned in the issue ✅
        2. Author reported the issue ✅
        3. Auther commenyed on the issue ✅

"""

# %%
from collections import UserList
from logging import raiseExceptions
from typing import List
import pandas as pd
import requests
import re
from tqdm import tqdm
import pickle
from colorama import Fore
import time
import os
import traceback
from dotenv import load_dotenv


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
print(ACCESS_TOKEN)

GH_API_URL = "https://api.github.com/repos/"

STATE = "all"
PER_PAGE = 100

HEADER = {"Authorization": "token " + ACCESS_TOKEN}

START_TIME = time.time()  # to get the time remaining for GH to allow requests :(


def format_url(url: str) -> str:
    """takes a github url and formats it to github api url"""
    url_split = url.split("/")
    return f"{GH_API_URL}{url_split[-2]}/{url_split[-1]}/pulls?state={STATE}&per_page={PER_PAGE}"


def format_url_issues(url: str, issue_num) -> str:
    url_split = url.split("/")
    return f"{GH_API_URL}{url_split[-2]}/{url_split[-1]}/issues/{issue_num}"


def format_comments_url(url: str) -> str:
    return f"{url}?per_page={PER_PAGE}"


def get_response(url, page) -> requests.Response:
    """makes a get request to the url with pagianation
    sleeps for 1 hour if requests exhausted

    """

    formatted_url = format_url(url)
    resp: requests.Response = requests.get(
        f"{formatted_url}&page={page}", headers=HEADER
    )
    if resp.status_code == 403:
        # rem_time = 60 * 60 - (time.time() - START_TIME)
        rem_time = 60 * 45
        time.sleep(rem_time)
        print(
            Fore.LIGHTBLACK_EX
            + "WE ARE SLEEPING!"
            + Fore.LIGHTCYAN_EX
            + "for "
            + str(rem_time)
            + "s"
        )
        resp: requests.Response = requests.get(
            f"{formatted_url}&page={page}", headers=HEADER
        )

    return resp


def get_resp_without_pages(url):
    """performas a simple get request. used for getting issue"""

    resp: requests.Response = requests.get(url, headers=HEADER)

    if resp.status_code == 403:
        # rem_time = 60 * 60 - (time.time() - START_TIME)
        rem_time = 60 * 45
        time.sleep(rem_time)
        print(
            Fore.LIGHTBLACK_EX
            + "WE ARE SLEEPING!"
            + Fore.LIGHTCYAN_EX
            + "for "
            + str(rem_time)
            + "s"
        )
        resp: requests.Response = requests.get(url, headers=HEADER)

    return resp


def srch_for_author_in_comments(response_json: dict, author: str):
    """searches if auther commented"""

    comments_url = response_json["comments_url"]
    frmtd_cmmnts_url = format_comments_url(comments_url)
    page = 1
    resp: requests.Response = get_response(frmtd_cmmnts_url, page)

    resp_json = resp.json()
    while resp_json:

        for i,comment in enumerate(tqdm(
            response_json, desc=f"Iterating over the comments page {page}"
        )):
            # capping the comments count so that it's feasable to collect this data
            if i == 100:
                break
            if comment["user"]["login"] == author:
                print(Fore.GREEN + "Author's comment found")
                return 1
        page += 1
        # capping the page limit so that 150 max items i.e 5*30
        if page == 5:
            break
        resp: requests.Response = get_response(frmtd_cmmnts_url, page)
        resp_json = resp.json()

    print(Fore.RED + "No comment from author")
    return 0


def get_project_list(path) -> List:
    """
    Get the list of all the github projects
    """
    df = pd.read_csv(path)
    return df


def match_regex(s: str, regex="WIP") -> bool:
    """check if the regex exists in the str"""
    try:
        match = re.findall(regex, s, re.IGNORECASE)
        return match
    except TypeError:
        return False


def chk_for_WIP_in_title_n_body(response_json) -> int:
    """check if WIP is mentioned in the tile or the body"""

    # print(response_json)
    title = response_json["title"]
    body = response_json["body"]

    if match_regex(title):
        print(Fore.GREEN + "Found WIP")
        return 1
    elif match_regex(body):
        print(Fore.GREEN + "Found WIP")
        return 1
    else:
        return 0


def chk_if_author_assigned_to_pr(response_json) -> int:
    """check if the auther or someone else if asssighed

    https://docs.github.com/en/rest/reference/pulls
    """

    author = response_json["user"]["login"]

    # if author == response_json["assignee"]["login"]:
    #     print(Fore.GREEN + "Author assigned to the PR")
    #     return 1
    assignees = response_json["assignees"]
    if len(assignees) > 0:
        print(Fore.GREEN + "people are assigned")
        return 1
    else:
        return 0


def chk_if_author_reported_issue(issue_json: dict, author):
    """checcks if auther reported the issue"""

    issue_reported_by = issue_json["user"]["login"]

    if issue_reported_by == author:
        print(Fore.GREEN + "Author created the issue")
        return 1
    return 0


def chk_if_author_assigned_to_issue(issue_json: dict, author: str):
    """checks if author is assigned in the issue"""

    issue_assignee = issue_json["assignee"]["login"]

    if issue_assignee == author:
        print(Fore.GREEN + "Author assignmed in issue")
        return 1
    return 0


def chk_linked_issues(response_json: dict) -> int:
    """check if issues are linked and then search for presence of author in the issues"""
    author = response_json["user"]["login"]
    repo_url = response_json["head"]["repo"]["full_name"]
    title = response_json["title"]
    body = response_json["body"]
    issues_title = match_regex(title, regex=" #([0-9]+)") or []
    issues_body = match_regex(body, regex=" #([0-9]+)") or []

    merged_list = list(set(issues_title + issues_body))
    if merged_list:
        for issue in issues_body:
            issue_url = format_url_issues(repo_url, issue)

            issue_resp = get_resp_without_pages(issue_url)
            issue_json = issue_resp.json()
            author_assigned_in_issue = chk_if_author_assigned_to_issue(
                issue_json, author
            )
            if author_assigned_in_issue == 1:
                return 1

            author_reported_issue = chk_if_author_reported_issue(issue_json, author)
            if author_reported_issue:
                return 1

            author_in_issue_comments = srch_for_author_in_comments(issue_json, author)
            if author_in_issue_comments:
                return 1

    return 0


def chk_for_precomm_in_a_pr(pr: dict):
    """
    Check if pre communication in a pr
    """

    wip_in_pr = chk_for_WIP_in_title_n_body(pr)
    if wip_in_pr:
        return 1

    author_assigned_to_pr = chk_if_author_assigned_to_pr(pr)
    if author_assigned_to_pr:
        return 1

    author_linked_to_issue = chk_linked_issues(pr)
    if author_linked_to_issue:
        return 1

    return 0


def get_pre_comm_idx_frm_url(url: str):
    """
    Gets the pre communication index for a ph pj
    idx = Pr with pre communication / total Pr
    """

    total_prs = 0
    prs_w_pre_comm = 0

    page = 1  # page no of the gh PR list
    resp: requests.Response = get_response(url, page)

    resp_json = resp.json()

    while resp_json:

        total_prs += len(resp_json)

        for pr in tqdm(resp_json, desc=f"Iterating over the pr json page {page}"):
            prs_w_pre_comm += chk_for_precomm_in_a_pr(pr)

            page += 1

            # capping page to 5 so O(n) = 5x30 = 150
            if page == 5:
                break
            resp: requests.Response = get_response(url, page)

    print(Fore.YELLOW + f"total pr {total_prs}")
    print(Fore.YELLOW + f"pr with pre comminication {prs_w_pre_comm}")

    try:
        ratio = prs_w_pre_comm / total_prs
        return ratio

    except ZeroDivisionError:
        return 0


# def get_cntrl_mng_idx_frm_url(url):
#     """gets the central management indes for a gh pj
#     idx = PRs with issues/total PRs
#     """

#     page = 1  # page number of the gh pr list
#     resp: requests.Response = get_response(url, page)

#     resp_json = resp.json()
#     total_prs = 0
#     prs_w_cntl_mng = 0
#     while resp_json:

#         total_prs += len(resp_json)

#         for pr in tqdm(resp_json, desc=f"Iterating over the pr json page {page}"):
#             prs_w_cntl_mng += chk_for_issue_in_title_n_body(pr)

#         page += 1
#         resp: requests.Response = get_response(url, page)
#         resp_json = resp.json()

#     print(Fore.YELLOW + f"total pr {total_prs}")
#     print(Fore.YELLOW + f"pr with issues {prs_w_cntl_mng}")

#     try:
#         ratio = prs_w_cntl_mng / total_prs
#         return ratio
#     except ZeroDivisionError:
#         return 0


def run_precomm_idx_for_all(path):
    """
    run the pre communication index for all the projects
    """

    precomm_idx_list = []

    df = pd.read_csv(path)
    for index, row in tqdm(df.iterrows()):
        print(Fore.LIGHTBLUE_EX + f"Processing {row['pj_alias']}")
        if not row["correct_url_found"]:
            # cntrl_mng_idx_list.append(None)
            print(Fore.RED + f"Running metric on mirrored url {row['pj_alias']}")

        try:
            precomm_idx = get_pre_comm_idx_frm_url(row["corrected_pj_github_url"])
        except Exception as e:
            print(e)
            print(row["corrected_pj_github_url"])
            traceback.print_exc()
            precomm_idx = None
            with open("output3.pickle", "wb") as f:
                pickle.dump(precomm_idx_list, f)

        precomm_idx_list.append(precomm_idx)

        print(Fore.LIGHTGREEN_EX + f"Done {row['pj_alias']}")

    with open("output3.pickle", "wb") as f:
        pickle.dump(precomm_idx_list, f)

    print("\n################### DONE ##################\n")
    print(precomm_idx_list)


def main():
    path = "./csvs/asfi_refined_with_metrics.csv"
    run_precomm_idx_for_all(path)


if __name__ == "__main__":
    main()
# %%
