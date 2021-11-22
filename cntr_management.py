"""centralized management index"""

# %%
from collections import UserList
from typing import List
import pandas as pd
import requests
import re
from tqdm import tqdm
import pickle
from colorama import Fore
import time
import os
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


def get_project_list(path) -> List:
    """
    Get the list of all the github projects
    """
    df = pd.read_csv(path)
    return df


def match_regex(s: str) -> bool:
    """check if the regex exists in the str"""
    regex = " #[0-9]*" # its seen that a reference can be made to an issue which is hosted at places other than github
    try:
        match = re.search(regex, s)
        return match
    except TypeError:
        return False


def chk_for_issue_in_title_n_body(response_json) -> int:
    """check if issue is mentioned in the response json"""
    title = response_json["title"]
    body = response_json["body"]

    if match_regex(title):
        return 1
    elif match_regex(body):
        return 1
    else:
        return 0


def get_response(url, page) -> requests.Response:
    """makes a get request to the url
    sleeps for 1 hour if requests exhausted

    """

    formatted_url = format_url(url)
    resp: requests.Response = requests.get(
        f"{formatted_url}&page={page}", headers=HEADER
    )
    if resp.status_code == 403:
        rem_time = 60 * 60 - (time.time() - START_TIME)
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


def get_cntrl_mng_idx_frm_url(url):
    """gets the central management indes for a gh pj
    idx = PRs with issues/total PRs
    """

    page = 1  # page number of the gh pr list
    resp: requests.Response = get_response(url, page)

    resp_json = resp.json()
    total_prs = 0
    prs_w_cntl_mng = 0
    while resp_json:

        total_prs += len(resp_json)

        for pr in tqdm(resp_json, desc=f"Iterating over the pr json page {page}"):
            prs_w_cntl_mng += chk_for_issue_in_title_n_body(pr)

        page += 1
        resp: requests.Response = get_response(url, page)
        resp_json = resp.json()

    print(Fore.YELLOW + f"total pr {total_prs}")
    print(Fore.YELLOW + f"pr with issues {prs_w_cntl_mng}")

    try:
        ratio = prs_w_cntl_mng / total_prs
        return ratio
    except ZeroDivisionError:
        return 0


def run_cntrl_mng_idx_for_all(path):
    """
    run the centralized management index for all the projects
    """

    cntrl_mng_idx_list = []

    df = pd.read_csv(path)
    for index, row in tqdm(df.iterrows()):
        print(Fore.LIGHTBLUE_EX + f"Processing {row['pj_alias']}")
        if not row["correct_url_found"]:
            # cntrl_mng_idx_list.append(None)
            print(Fore.RED + f"Running metric on mirrored url {row['pj_alias']}")
            

        try:

            cntrl_idx = get_cntrl_mng_idx_frm_url(row["corrected_pj_github_url"])
        except Exception as e:
            print(e)
            print(row["corrected_pj_github_url"])
            # cntrl_mng_idx_list.append(None)
            cntrl_idx = None
            with open("output2.pickle", "wb") as f:
                pickle.dump(cntrl_mng_idx_list, f)

        cntrl_mng_idx_list.append(cntrl_idx)

        print(Fore.LIGHTGREEN_EX + f"Done {row['pj_alias']}")

    with open("output2.pickle", "wb") as f:
        pickle.dump(cntrl_mng_idx_list, f)

    print("################### DONE ##################")
    print(cntrl_mng_idx_list)


def main():
    path = "./csvs/asfi_refined_with_metrics.csv"
    run_cntrl_mng_idx_for_all(path)


if __name__ == "__main__":
    main()
# %%
