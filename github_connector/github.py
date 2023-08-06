import requests


class GithubConnector:
    def __init__(self, access_token, url):
        self.__access_token = access_token
        self.url = url

    def get_issues_by_repo(self, repo_name):
        url = f"{self.url}/repos/{repo_name}/issues"
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
                    "html_url": issue["html_url"],
                }
                for issue in issues
            ]
            return issues
        else:
            return None
