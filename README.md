## Forking Around: Correlation of forking practices with the success of a project

Ongoing project on finding the corelation between efficient forking practices and the success/failure of a project using ASFI dataset. 

We have calculated a set of eight metrics:

### Metric 1
**Logic coupling Index:** is used to assess the modularity of the project by analyzing the most recent commits by contributors. We estimate the ratio of file pairs that were changed, i.e. added or modified, together in those commits out of all file pairs in the projects using PyDriller. Next, by computing the mean of recent commits, we aggregate this metric at the project level. We assess the most recent 150 commits for each project in order to remove bias from past but now altered practices. Lower logic coupling indexes suggest higher modularity, as fewer files are altered at the same time.

File: [src/Logic_coupling_index.py](src/Logic_coupling_index.py)

### Metric 2
**Additive contribution Index:** is a second modularity measure that assesses the extent to which contributions are additive, i.e contributions by adding files rather than editing existing ones. We calculate the ratio of new files added out of all files modified per commit, extracted through PyDriller. For a project, it’s the average ratio of overall commits from contributors. Higher additive contribution index shows that more modifications were additive in nature, implying a stronger modularity from the viewpoint of contributors.

File: [src/Additivie_coupling_index.py](src/Additivie_coupling_index.py)

### Metric 3 
**Ratio of Duplicate PRs:** is a clear metric for redundant work. We measure the fraction of the closed PRs rejected, by maintainers, stating as being redundant. We use GitHub API to fetch the attributes of the PR requests. To identify duplicate PRs in a project, we use regex matching and look for comments in the PR such as ‘duplicated’, ‘superseded’, ‘replicated’, etc. in PR comments.

File: [metrics_hardforks_duplicatePRs.py](metrics_hardforks_duplicatePRs.py)

### Metric 4
**Presence of hard forks:** a fork that has at least 2 merged pull requests from external developers is identified as a hard fork. For calculating this metric, we use the REST API by GitHub to get a list of forks, and for each fork, we get a list of pull requests. Then, we see the merge status of each pull request in that fork to categorize if there are any merged PRs in a particular fork. If we find 2 or more merged PRs for a fork, we assign a boolean value of TRUE/FALSE for that project categorizing if the project has a hard fork or not.

File: [metrics_hardforks_duplicatePRs.py](metrics_hardforks_duplicatePRs.py)

### Metric 5
**Centralized management Index:** measures the fraction of PRs that link to issues out of all PRs from all contributors. The list of PRs is fetched using GitHub API for a project and regex is used to search for keywords like ‘issue #123’ or ‘#123’ in the title, comments, and/or git messages. Some projects refer to issues not hosted on GitHub. The reference, however, still follows the convention of starting with '#'.

File: [cntr_management.py](cntr_management.py)

### Metric 6
**Pre-communication index:** observes the coordination amongst the developers and contributors. in this metric, we look for the public announcement made by the contributors regarding the issue they are working on.
We do this in a hierarchical order. We first look for the announcement on the PR, then we look for if the author is one of the assignees of the PR. Next, we check if the PR is linked to an issue and parse these issues to check if the author has been assigned the issue or if the author has raised the issue. Finally, we check the comments in the linked issue for traces of participation by the author of the PR.

File: [pre_communication.py](pre_communication.py)

### Metric 7
**Dimensionality Index:** measures the size of commits, more precisely average lines of code changes (added + deleted) per file per commit in a project. This metric tries to capture the distribution of the size of commits between successful and failed projects.  We used PyDriller and traverse all commits pushed by developers to a project to get the lines of code changed per commit. The dimensionality index value for a project is the average of lines of code changed to the number of files changed across all commits.

File: [src/metrics.py](src/metrics.py)

### Metric 8
**Frequency Index:** is a metric to take into account the rate of contributions made by developers to a project and the degree as to how difficult it is for the core team to incorporate the changes. It's measured as the average number of PRs raised to the main branch in a particular time interval. We decided on an initial time interval of 14 days for collecting this metric. Noticing a great variability in the data collected we then decided to check the number of PRs raised during a month. Since PyDriller does not have pull requests data we rely on GitHub APIs to collect them for a project. Using paginated pull APIs we get all the PRs and count the number of PRs raised during a period of 30 days. The index value is then just the average of the counts of all the PRs raised. 

File: [src/metrics.py](src/metrics.py)

### Results

The results of these metrics calculation can be found here: [results/metrics_combined_asfi_refined_with_metrics.csv](results/metrics_combined_asfi_refined_with_metrics.csv)
