from numpy import NaN
import requests
import pandas as pd
import re
import time

#personal token
token = ""
headers = {
	"Authorization": "token " + token
}

##Todo
##external developers - 
# check for external contributor
# i will take any contributor other than apache to be external contributor
#if resp['user']['login'] != "apache":
##optimization

def get_repos():
	df = pd.read_csv("csv/asfi_refined_false_removed.csv")
	project_list = []
	#project_list = ["https://api.github.com/repos/apache/incubator-Gobblin"]
	project_list = df.pj_github_api_url
	print("No. of projects:", len(project_list))
	return project_list

def get_forks(project):
	page_num = 1
	path = project+"/forks?page={}&per_page=100".format(page_num)

	resp = requests.get(path, headers=headers)
	resp.raise_for_status()
	resp_json = resp.json()

	forks_url = []

	for resp in resp_json:
		forks_url.append(resp['url'])
		
	while(len(resp_json) == 100):
		page_num = page_num + 1
		path = project+"/forks?page={}&per_page=100".format(page_num)

		resp= requests.get(path, headers=headers)
		resp.raise_for_status()
		resp_json = resp.json()

		for resp in resp_json: 
			forks_url.append(resp['url'])
		
	print("Total No. of Forks:", len(forks_url))
	return forks_url

def get_pulls(url):
	page_num = 1
	path = url+"/pulls?page={}&per_page=100&state=closed".format(page_num)

	resp = requests.get(path, headers=headers)
	resp.raise_for_status()
	resp_json = resp.json()

	pulls_url = []

	for resp in resp_json:
		pulls_url.append(resp['url'])
		
	while(len(resp_json) == 100):
		page_num = page_num + 1
		path = url+"/pulls?page={}&per_page=100&state=closed".format(page_num)
		
		resp = requests.get(path, headers=headers)
		resp.raise_for_status()
		resp_json = resp.json()

		for resp in resp_json:
			pulls_url.append(resp['url'])
		
	#print("Total No. of pulls:", len(pulls_url))
	return pulls_url
	
def get_merge_status(pull_url):
	response = requests.get(pull_url+"/merge", headers=headers)
	merge_status = response.status_code
	print(merge_status)
	return merge_status

## Metric 1 - Presence of hard forks
def check_for_hard_forks():
	df = pd.read_csv("csv/asfi_refined_false_removed.csv")
	df['has_hard_fork'] = NaN
	df['total_hard_forks'] = NaN
	df['total_forks'] = NaN

	repos = get_repos()
	for repo in repos:
		calculated = float(df.loc[df['pj_github_api_url'] == repo, 'total_forks'])
		if calculated >= 0.0:
			continue
		
		total_hard_forks = 0
		try:
			forks = get_forks(repo)
			total_forks = len(forks)
			df.loc[df['pj_github_api_url'] == repo, 'total_forks'] = total_forks
			
			if total_forks == 0:
				is_hard_fork = False
				df.loc[df['pj_github_api_url'] == repo, 'has_hard_fork'] = is_hard_fork
				df.loc[df['pj_github_api_url'] == repo, 'total_hard_forks'] = total_hard_forks
				continue
			
			for fork in forks:
				merged_pr = 0
				try:
					pulls_data = get_pulls(fork)
					total_prs = len(pulls_data)
					if (total_prs == 0):
						is_hard_fork = False
						df.loc[df['pj_github_api_url'] == repo, 'has_hard_fork'] = is_hard_fork
						df.loc[df['pj_github_api_url'] == repo, 'total_hard_forks'] = total_hard_forks
						continue
					for pull_request in pulls_data:
						merge_status = get_merge_status(pull_request)
						## PR is successfully merged
						if merge_status == 204:
							print("Merged PR")
							merged_pr += 1
					print(merged_pr)
					if merged_pr >= 2:
						is_hard_fork = True
						total_hard_forks += 1
						df.loc[df['pj_github_api_url'] == repo, 'has_hard_fork'] = is_hard_fork
						df.loc[df['pj_github_api_url'] == repo, 'total_hard_forks'] = total_hard_forks
						print(fork, is_hard_fork)
						df.to_csv("csv/asfi_refined_false_removed.csv", index=False)
				
				except Exception as e: 
					print("Fork Failed:", fork)
					print('{}'.format(e))
					pass

		except Exception as e: 
			print("Repo Failed:", repo)
			print('{}'.format(e))
			pass

		print(repo, is_hard_fork)
		df.to_csv("csv/asfi_refined_false_removed.csv", index=False)

def get_comments(pull_url):
	page_num = 1
	response = requests.get(pull_url+"/comments", headers=headers).json()
	resp_json = response
	comments_list = []
	
	for resp in resp_json: 
		comments_list.append(resp["body"])
	return comments_list

def pattern_matching(comment):
	
	pattern = r"(clos(e|ed|ing)|dup(licate(d)?|e)?|super(c|s)ee?ded?|obsoleted?|replaced|redundant|better(implementation|solution)|already(solved|addressed)|(solved|addressed)already)|fixed already"
	result = re.match(pattern, comment)
	duplicate_pr = 0

	if result: 
		duplicate_pr += 1
	else:
		pass
	
	return duplicate_pr

## Metric 2 - Ratio of duplicate PRs
def ratio_of_duplicate_prs():
	df = pd.read_csv("csv/asfi_refined_false_removed.csv")
	# df['ratio_of_duplicate_prs'] = NaN
	# df['total_prs'] = NaN
	# df['duplicate_prs'] = NaN

	repos = get_repos()
	for repo in repos:
		calculated = float(df.loc[df['pj_github_api_url'] == repo, 'total_prs'])
		if calculated >= 0.0:
			continue
		
		duplicate_prs = 0
		try:
			print(repo)
			pulls_data = get_pulls(repo)
			total_prs = len(pulls_data)
			print("Total PRs: ", total_prs)
			if total_prs == 0:
				ratio = 0
				df.loc[df['pj_github_api_url'] == repo, 'ratio_of_duplicate_prs'] = ratio
				df.loc[df['pj_github_api_url'] == repo, 'total_prs'] = total_prs
				df.loc[df['pj_github_api_url'] == repo, 'duplicate_prs'] = duplicate_prs
				continue

			for pull_request in pulls_data:
				comments = get_comments(pull_request)
				for comment in comments:
					dup = pattern_matching(comment)
					duplicate_prs += dup
				# print (duplicate_prs)

			ratio = duplicate_prs / total_prs
			df.loc[df['pj_github_api_url'] == repo, 'ratio_of_duplicate_prs'] = ratio
			df.loc[df['pj_github_api_url'] == repo, 'total_prs'] = total_prs
			df.loc[df['pj_github_api_url'] == repo, 'duplicate_prs'] = duplicate_prs
			print(repo, ratio, "=", duplicate_prs , "/", total_prs)

		except Exception as e: 
			print("Repo Failed:", repo)
			print('{}'.format(e))
			pass

		df.to_csv("csv/asfi_refined_false_removed.csv", index=False)

def check_rate_limit():
	resp = requests.get("https://api.github.com/rate_limit", headers=headers).json()
	#print(resp)
	print(resp["rate"])

check_rate_limit()
#check_for_hard_forks()
ratio_of_duplicate_prs()
#get_forks("https://api.github.com/repos/apache/incubator-Gobblin")
#get_pulls("https://api.github.com/repos/apache/incubator-retired-amaterasu")
#get_comments("")
#get_merge_status("https://api.github.com/repos/Diffblue-benchmarks/gobblin/pulls/2")

#Testing
#get_forks("https://api.github.com/repos/apache/incubator-retired-amaterasu")
#get_pulls("https://api.github.com/repos/apache/incubator-BRPC/forks")
#total_prs = len(get_pulls("https://api.github.com/repos/apache/incubator-retired-amaterasu"))
#url = "https://api.github.com/repos/xap/xap"
#for comment in get_comments(url+"/pulls"):
#	duplicate_prs = pattern_matching(comment)
#print(len(get_pulls(url)))
#print(duplicate_prs)
