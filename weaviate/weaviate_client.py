import weaviate


class Weaviate:
    def __init__(self, cluster_url, bearer_token, api_key):
        self.cluster_url = cluster_url
        self.__bearer_token = bearer_token
        self.__api_key = api_key
        auth_config = weaviate.auth.AuthApiKey(api_key=bearer_token)
        client = weaviate.Client(
            url=cluster_url,
            auth_client_secret=auth_config,
            additional_headers={
                "X-OpenAI-Api-Key": api_key,
            },
        )
        self.__client = client

    def search_issue(self, repo_id, issue_number):
        data = (
            self.__client.query.get("Issue", ["id"])
            .with_where(
                {
                    "operator": "And",
                    "operands": [
                        {
                            "path": ["repo_id"],
                            "operator": "Equal",
                            "valueInt": repo_id,
                        },
                        {
                            "path": ["issue_number"],
                            "operator": "Equal",
                            "valueInt": issue_number,
                        },
                    ],
                },
            )
            .with_limit(1)
            .do()
        )

        if data["data"]["Get"]["Issue"] == []:
            return False, -1
        return True, data["data"]["Get"]["Issue"][0]["id"]

    def update_issue(self, issue_uid, issue_title, issue_description):
        self.__client.data_object.update(
            uuid=issue_uid,
            class_name="Issue",
            data_object={"title": issue_title, "description": issue_description},
        )

    def create_issue(self, object):
        uuid = self.__client.data_object.create(object, "Issue")
        return uuid
