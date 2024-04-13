import requests
import logging

logger = logging.getLogger(__name__)

class GitHubAPIClient:
    def __init__(self, token: str, base_api_url: str) -> None:
        self.token = token
        self.base_api_url = base_api_url.rstrip("/")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self.token}",
        }
    
    def execute_api_call(self, method: str, endpoint: str, data: dict = None) -> dict:
        
        url = f"{self.base_api_url}/{endpoint}"
        
        if data is None:
            response = requests.request(method, url, headers=self.headers)
        else:
            response = requests.request(method, url, headers=self.headers, json=data)
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        elif response.status_code == 204:
            return {}
        else:
            raise Exception(f"Failed to execute API call: {response.text}")
    
    def get_org_repos(self, organisation: str) -> dict:
        return self.execute_api_call("GET", f"orgs/{organisation}/repos")
    
    def get_user_repos(self, user: str) -> dict:
        return self.execute_api_call("GET", f"users/{user}/repos")
    
    def list_webhooks(self, owner: str, repo: str) -> dict:
        return self.execute_api_call("GET", f"repos/{owner}/{repo}/hooks")
    
    def create_webhook(self, owner: str, repo: str, webhook_url: str) -> dict:
        logger.info(f"Creating webhook for {owner}/{repo}")

        data = {
            "name": "web",
            "active": True,
            "events": ["push"],
            "config": {
                "url": webhook_url,
                "content_type": "json",
            },
        }
        
        return self.execute_api_call("POST", f"repos/{owner}/{repo}/hooks", data)
    
    def delete_webhook(self, owner: str, repo: str, webhook_id: int) -> dict:
        logger.info(f"Deleting webhook {webhook_id} from {owner}/{repo}")

        return self.execute_api_call("DELETE", f"repos/{owner}/{repo}/hooks/{webhook_id}")