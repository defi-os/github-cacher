import configparser
from github_connector.github import GithubConnector
from weaviate.weaviate_client import Weaviate
import time

config = configparser.ConfigParser()
config.read("../config.ini")

weaviate_cluster_url = config["WEAVIATE"]["CLUSTER_URL"]
weaviate_bearer_token = config["WEAVIATE"]["BEARER_TOKEN"]
open_ai_api_key = config["OPENAI"]["API_KEY"]
github_key = config["GITHUB"]["BEARER_TOKEN"]
github_url = config["GITHUB"]["GITHUB_URL"]
threshhold = config["GITHUB"]["THRESHHOLD"]
github = GithubConnector(github_key, github_url)
weaviate_client = Weaviate(weaviate_cluster_url, weaviate_bearer_token, open_ai_api_key)

page = 1
per_page = 100
loop = True

while loop:
    repos = github.search_repo_by_langauge("Rust", page, per_page)
    if repos is None:
        time.sleep(5)
        continue
    if repos == []:
        loop = False
        break
    filtered_repos = github.filter_repositories("Rust",repos, threshhold)
    for repo in filtered_repos:
        issues = github.get_issues_by_repo(repo["id"])
        if issues is None:
            time.sleep(5)
            continue
        for issue in issues:
            exists, weaviate_uid = weaviate_client.search_issue(
                repo["id"], issue["number"]
            )
            if exists:
                weaviate_client.update_issue(
                    weaviate_uid, issue["title"], issue["description"]
                )
            else:
                issue_object = {
                    "title": issue["title"],
                    "description": issue["description"],
                    "repo_id": int(repo["id"]),
                    "issue_number": int(issue["number"]),
                }
                weaviate_client.create_issue(issue_object)
    page += 1
