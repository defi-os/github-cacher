import weaviate
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")

weaviate_cluster_url = config["WEAVIATE"]["CLUSTER_URL"]
weaviate_bearer_token = config["WEAVIATE"]["BEARER_TOKEN"]
open_ai_api_key = config["OPENAI"]["API_KEY"]

auth_config = weaviate.auth.AuthApiKey(api_key=weaviate_bearer_token)
client = weaviate.Client(
    url=weaviate_cluster_url,
    auth_client_secret=auth_config,
    additional_headers={"X-OpenAI-Api-Key": open_ai_api_key},
)


class_obj = {
    "class": "Issue",
    "description": "Github Issues",
    "properties": [
        {"dataType": ["text"], "description": "Title of the issue", "name": "title"},
        {
            "dataType": ["text"],
            "description": "Description of issue",
            "name": "description",
        },
        {"dataType": ["int"], "description": "Repo of issue", "name": "repo_id"},
        {"dataType": ["int"], "description": "issue_number"},
    ],
    "vectorizer": "text2vec-openai",
}

client.schema.create_class(class_obj)
