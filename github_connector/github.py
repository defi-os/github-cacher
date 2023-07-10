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

        if response.status_code != 200:
            return None
        if "items" not in data:
            return []
        repos = [
            {"id": repo["id"], "languages_url": repo["languages_url"]}
            for repo in data["items"]
        ]
        return repos

    @staticmethod
    def calculate_langauge_percentage(langauge, languages_data):
        total_bytes = sum(languages_data.values())
        rust_bytes = languages_data.get(langauge, 0)

        if total_bytes > 0:
            return rust_bytes / total_bytes
        else:
            return 0.0

    @staticmethod
    def filter_repositories(langauge, repositories, threshold):
        filtered_repos = []
        for repo in repositories:
            repo_id = repo["id"]
            languages_url = repo["languages_url"]
            try:
                response = requests.get(languages_url)
                languages_data = response.json()
                rust_percentage = GithubConnector.calculate_langauge_percentage(
                    langauge, languages_data
                )
            except:
                continue
            if rust_percentage >= threshold:
                filtered_repos.append(repo_id)

        return filtered_repos

    def get_issues_by_repo(self, repo_id):
        url = f"{self.url}/repositories/{repo_id}/issues"
        headers = {
            "Accept": "application/vnd.github.mercy-preview+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self.__access_token}",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            issues = response.json()
            issues = [
                {
                    "title": issue["title"],
                    "description": issue["body"],
                    "number": issue["url"].split("issues/")[1],
                }
                for issue in issues
            ]
            return issues
        else:
            return None
