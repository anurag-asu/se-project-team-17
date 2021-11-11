import os
import pandas as pd

from download_helper import get_download_links, get_downloaded_repos

from constants import FAILED_URLS_CORRECTED, FAILED_URLS


def refine_dataset():
    df = pd.read_csv("csvs/asfi_copy.csv")

    df = df[["pj_alias", "status", "pj_github_url"]]
    df["corrected_pj_github_url"] = ""
    df["correct_url_found"] = False

    links = get_download_links()
    repos = get_downloaded_repos()

    for link in links:
        base_name = os.path.basename(link)
        if base_name in repos:
            df.loc[df["pj_github_url"] == link, "corrected_pj_github_url"] = link
            df.loc[df["pj_github_url"] == link, "correct_url_found"] = True

    for i in range(len(FAILED_URLS)):
        failed_url = FAILED_URLS[i]
        failed_url_corrected = FAILED_URLS_CORRECTED[i]

        df.loc[
            df["pj_github_url"] == failed_url, "corrected_pj_github_url"
        ] = failed_url_corrected
        df.loc[df["pj_github_url"] == failed_url, "correct_url_found"] = (
            failed_url != failed_url_corrected
        )

    df.to_csv("asfi_refined.csv")
    print(df.head)


# refine_dataset()
