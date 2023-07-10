import configparser
from github_connector.github import GithubConnector
from weaviate.weaviate_client import Weaviate

config = configparser.ConfigParser()
config.read("config.ini")

weaviate_cluster_url = config["WEAVIATE"]["CLUSTER_URL"]
weaviate_bearer_token = config["WEAVIATE"]["BEARER_TOKEN"]
open_ai_api_key = config["OPENAI"]["API_KEY"]
github_key = config["GITHUB"]["BEARER_TOKEN"]
github_url = config["GITHUB"]["GITHUB_URL"]

github = GithubConnector(github_key, github_url)
weaviate = Weaviate(weaviate_cluster_url,weaviate_bearer_token,open_ai_api_key)
