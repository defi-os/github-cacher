import requests


class GithubConnector:
    def __init__(self, access_token, url):
        self.__access_token = access_token
        self.url = url

    def search_repo_by_langauge(self, lang, page, per_page):
        headers = {
            "Accept": "application/vnd.github.mercy-preview+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self.__access_token}",
        }
        query = f"language:{lang}"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }

        response = requests.get(
            f"{self.url}/search/repositories", params=params, headers=headers
        )
        data = response.json()

        if response.status_code != 200 or "items" not in data:
            return []
        return data["items"]

    @staticmethod
    def calculate_rust_percentage(languages_data):
        total_bytes = sum(languages_data.values())
        rust_bytes = languages_data.get("Rust", 0)

        if total_bytes > 0:
            return rust_bytes / total_bytes
        else:
            return 0.0

    @staticmethod
    def filter_rust_repositories(repositories, threshold):
        filtered_repos = []
        for repo in repositories:
            repo_url = repo["html_url"]
            repo_name = repo["name"]
            languages_url = repo["languages_url"]

            response = requests.get(languages_url)
            languages_data = response.json()
            rust_percentage = GithubConnector.calculate_rust_percentage(languages_data)
            if rust_percentage >= threshold:
                filtered_repos.append((repo_name, repo_url))

        return filtered_repos
