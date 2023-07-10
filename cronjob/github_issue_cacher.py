import weaviate
import configparser
from github_cacher.github_connector.github import GithubConnector

config = configparser.ConfigParser()
config.read("config.ini")

weaviate_cluster_url = config["WEAVIATE"]["CLUSTER_URL"]
weaviate_bearer_token = config["WEAVIATE"]["BEARER_TOKEN"]
open_ai_api_key = config["OPENAI"]["API_KEY"]
github_key = config["GITHUB"]["BEARER_TOKEN"]
github_url = config["GITHUB"]["GITHUB_URL"]

auth_config = weaviate.auth.AuthApiKey(api_key=weaviate_bearer_token)
client = weaviate.Client(
    url=weaviate_cluster_url,
    auth_client_secret=auth_config,
    additional_headers={"X-OpenAI-Api-Key": open_ai_api_key},
)

github = GithubConnector(github_key, github_url)
