import os
import logging

import pandas as pd
from pathlib import Path
from pydriller import Repository

from constants import FAILED_URLS_SET_1


logger = logging.getLogger(__name__)


def get_download_links():
    df = pd.read_csv("csvs/metrics_combined_copy.csv")
    return list(df["corrected_pj_github_url"])


def get_download_dir():
    download_dir = Path("local_repos")
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


def download_repo_through_pydriller(downloadDir, link):

    try:
        for commit in Repository(
            path_to_repo=link, clone_repo_to=downloadDir
        ).traverse_commits():
            pass
    except Exception as e:
        logger.error("Download failed for link {} with error".format(link, e))
        raise e


def get_downloaded_repos():
    my_list = os.listdir("local_repos")
    return my_list


def failed_links_count():
    repos = get_downloaded_repos()
    links = get_download_links()
    failed = []
    for link in links:
        if os.path.basename(link) not in repos:
            print(str(os.path.basename(link)).lower())
            failed.append(link)

    # print(failed)
    print(failed)
    print(len(repos))
    print(len(links))
    print(len(FAILED_URLS_SET_1))


def download_single():
    download_repo_through_pydriller(
        "local_repos", "https://github.com/apache/logging-log4cxx"
    )


# download_single()
