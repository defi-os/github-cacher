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
        params = {
            "per_page": 100,  # Maximum number of results per page (max 100)
            "page": 1,  # Page number of the results to fetch (start from page 1)
            "state": "open",
        }

        all_issues = []
        while True:
            print(params["page"])
            response = requests.get(url, headers=headers, params=params)
            print(response.json())
            if response.status_code == 200:
                issues = response.json()
                if not issues or issues == []:  # No more issues left
                    break
                all_issues.extend(
                    [
                        {
                            "title": issue["title"],
                            "description": issue["body"],
                            "html_url": issue["html_url"],
                        }
                        for issue in issues
                    ]
                )
                params["page"] += 1  # Move to the next page for the next request

        return all_issues
