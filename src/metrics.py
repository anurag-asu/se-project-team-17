import os
from numpy import NaN

import pandas as pd
from pydriller import Repository

from datetime import date, time, datetime, timedelta

from download_helper import get_downloaded_repos, get_download_links

# size of commits 
def collect_dimensionality_metric():
    try:
        repos = get_downloaded_repos()
        links = get_download_links()

        df = pd.read_csv('csvs/asfi_refined.csv')
        df['dimensionality'] = NaN

        for link in links:
            if os.path.basename(link) in repos:
                repo = os.path.basename(link)
                
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
                print(repo, dimensionality)
        
        df.to_csv('csvs/asfi_refined.csv')

    except Exception as e:
        print('error collect_dimensionality_metric = {}'.format(e))


# frequency of commits 
def collect_frequency_index(num_days):
    try:
        repos = get_downloaded_repos()
        links = get_download_links()

        df = pd.read_csv('csvs/asfi_refined.csv')
        df['frequency'] = NaN

        for link in links:
            if os.path.basename(link) in repos:
                repo = os.path.basename(link)
            
                for commit in Repository('local_repos/{}'.format(repo), order='reverse').traverse_commits():
                    commit_start_date = commit.committer_date
                    break
                for commit in Repository('local_repos/{}'.format(repo)).traverse_commits():
                    commit_end_date = commit.committer_date
                    break

                start_date = date(year=commit_start_date.year, month=commit_start_date.month, day=commit_start_date.day)
                end_date = date(year=commit_end_date.year, month=commit_end_date.month, day=commit_end_date.day)

                start_range = start_date
                end_range = start_date.timedelta(days=num_days)
                commits_per_interval = []
 
                while(start_range <= end_date):
                    num_commits = 0
                    for commit in Repository('local_repos/{}'.format(repo), since=start_range, to=end_range).traverse_commits():
                        num_commits += 1

                    commits_per_interval.append(num_commits)
                    start_range = end_range.timedelta(days=1)
                    end_range = start_range.timedelta(days=num_days)
                
                avg_commits_per_range = sum(commits_per_interval)/len(commits_per_interval)
                df[df['corrected_pj_github_url'] == link, 'frequency'] = avg_commits_per_range
            
        df.to_csv('csvs/asfi_refined.csv')

    except Exception as e:
        print('error collect_frequency_index = {}'.format(e))

# collect_frequency_index(14)

collect_dimensionality_metric()