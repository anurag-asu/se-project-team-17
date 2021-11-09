# %%
import pandas as pd
import requests
from pathlib import Path

from tqdm import tqdm


def find_dead_github_links(database_csv: Path) -> pd.DataFrame:
    """finds all the un responsive github links"""

    # the utf-8 encoding was givving some error
    database_df = pd.read_csv(database_csv, encoding="latin-1")
    nonresp_proj = {"listid": [], "pj_alias": [], "github_url": []}
    for i in tqdm(
        list(
            zip(
                list(database_df["listid"]),
                list(database_df["pj_alias"]),
                list(database_df["pj_github_url"]),
            )
        ),
        desc="Fetching github links",
    ):
        resp = requests.get(i[2])
        if resp.status_code != 200:
            nonresp_proj["listid"].append(i[0])
            nonresp_proj["pj_alias"].append(i[1])
            nonresp_proj["github_url"].append(i[2])

    return pd.DataFrame(nonresp_proj)


# %%


if __name__ == "__main__":
    datbase_csv = "./lists_2019_8.csv"
    nonresp_proj_df = find_dead_github_links(datbase_csv)
    nonresp_proj_df.to_csv("nonresp_proj.csv")
