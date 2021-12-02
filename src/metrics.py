import os
import requests
from urllib import parse
from numpy import NaN

import pandas as pd
from pydriller import Repository
from urllib.parse import urlparse

from datetime import date, time, datetime, timedelta

from download_helper import get_downloaded_repos, get_download_links
from global_constants import TOKEN

#size of commits 
def collect_dimensionality_metric():
    try:
        repos = get_downloaded_repos()
        links = get_download_links()

        df = pd.read_csv('csvs/metrics_combined_copy.csv')
        # df['dimensionality'] = NaN

        for link in links:

            found = df.loc[df['corrected_pj_github_url'] == link, 'correct_url_found'].bool()
            if not found:
                df.loc[df['corrected_pj_github_url'] == link, 'dimensionality'] = NaN
                df.to_csv('csvs/metrics_combined_copy.csv', index=False)
                continue

            if os.path.basename(link) in repos:

                value = float(df.loc[df['corrected_pj_github_url'] == link, 'dimensionality'])
                if value > 0.0:
                    continue

                repo = os.path.basename(link)

                print('calculating for link', link)
                
                commits_nums = 0
                dimensionality = 0
                for commit in Repository('local_repos/{}'.format(repo)).traverse_commits():
                    if not commit.lines or not commit.files:
                        continue

                    commits_nums += 1
                    dimensionality += (commit.lines/commit.files)
                
                print(commits_nums, dimensionality)
                if commits_nums:
                    dimensionality /= commits_nums
                else:
                    print(repo, commits_nums, dimensionality)

                df.loc[df['corrected_pj_github_url'] == link, 'dimensionality'] = dimensionality
                df.to_csv('csvs/metrics_combined_copy.csv')
                print(repo, dimensionality)

    except Exception as e:
        print('error collect_dimensionality_metric = {}'.format(e))


def get_pulls(repoLink):
    url_obj = urlparse(repoLink)
    page_num = 1
    path = "https://api.github.com/repos{}/pulls?sort=created&direction=asc&page={}&per_page=100&state=all".format(url_obj.path, page_num)
    
    resp = requests.get(path, headers={"Authorization": "token " + TOKEN})
    resp.raise_for_status()
    resp_json = resp.json()

    created_at = []

    for page_repsonse in resp_json:
        created_at.append(page_repsonse['created_at'])

    while(len(resp_json) == 100):
        page_num = page_num + 1
        path = "https://api.github.com/repos{}/pulls?sort=created&direction=asc&page={}&per_page=100&state=all".format(url_obj.path, page_num)

        resp = requests.get(path, headers={"Authorization" : "token " + TOKEN})
        resp.raise_for_status()
        resp_json = resp.json()


        for page_repsonse in resp_json:
            created_at.append(page_repsonse['created_at'])
    
    return created_at

# frequency of commits 
def collect_frequency_index(num_days):
    try:

        links = get_download_links()
        # links = ['https://github.com/apache/incubator-Doris']

        df = pd.read_csv('csvs/metrics_combined_copy.csv')

        for link in links:

            found = df.loc[df['corrected_pj_github_url'] == link, 'correct_url_found'].bool()
            if not found:
                df.loc[df['corrected_pj_github_url'] == link, 'frequency'] = NaN
                df.to_csv('csvs/metrics_combined_copy.csv', index=False)
                continue

            pr_found = df.loc[df['corrected_pj_github_url'] == link, 'prs_found'].bool()
            if not pr_found:
                df.loc[df['corrected_pj_github_url'] == link, 'frequency'] = 0
                df.to_csv('csvs/metrics_combined_copy.csv', index=False)
                continue

            try:

                freq = float(df.loc[df['corrected_pj_github_url'] == link, 'frequency'])
                if freq > 0.0:
                    continue

                print(link)

                created_at_list = get_pulls(link)
                print('created_at_list', len(created_at_list))


                if(len(created_at_list) == 0):
                    continue
                
                df.loc[df['corrected_pj_github_url'] == link, 'prs_found'] = True

                created_start_date = created_at_list[0]
                created_end_date= created_at_list[len(created_at_list)-1]

                created_start_date = datetime.strptime(created_start_date, '%Y-%m-%dT%H:%M:%SZ')
                created_end_date = datetime.strptime(created_end_date, '%Y-%m-%dT%H:%M:%SZ')


                start_date = datetime(year=created_start_date.year, month=created_start_date.month, day=created_start_date.day)
                end_date = datetime(year=created_end_date.year, month=created_end_date.month, day=created_end_date.day, hour=23, minute=59, second=59)

                start_range = start_date
                end_range = start_date + timedelta(days=num_days, hours=23, minutes=59, seconds=59)
                commits_per_interval = []

                while(start_range <= end_date):
                    count = 0
                    for created_at in created_at_list:
                        created_at_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
                        if created_at_date >= start_range and created_at_date <= end_range:
                            count += 1
                        
                    commits_per_interval.append(count)
                    start_range = datetime(year=end_range.year, month=end_range.month, day=end_range.day) + timedelta(days=1)
                    end_range = start_range + timedelta(days=num_days, hours=23, minutes=59, seconds=59)

                # print('commits per interval', sum(commits_per_interval), commits_per_interval)
                avg_commits_per_range = sum(commits_per_interval)/len(commits_per_interval)
                df.loc[df['corrected_pj_github_url'] == link, 'frequency'] = avg_commits_per_range
                df.to_csv('csvs/asfi_refined_with_metrics.csv', index=False)
            except Exception as e:
                print('error collect_frequency_index for link = {} with erro = {}'.format(link, e))

    except Exception as e:
        print('error collect_frequency_index = {}'.format(e))


collect_frequency_index(30)

# collect_dimensionality_metric()

# collect_frequency_and_dimensionality_index(14)