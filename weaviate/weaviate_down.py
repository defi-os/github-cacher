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
    additional_headers={
        "X-OpenAI-Api-Key": open_ai_api_key,
    },
)

client.schema.delete_all()
