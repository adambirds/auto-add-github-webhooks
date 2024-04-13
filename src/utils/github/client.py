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
    
    def execute_api_call(self, method: str, endpoint: str, params: dict = None, data: dict = None) -> dict:
        url = f"{self.base_api_url}/{endpoint}"
        
        if method == "GET" and params:
            response = requests.get(url, headers=self.headers, params=params)
        elif data:
            response = requests.post(url, headers=self.headers, json=data)
        else:
            response = requests.request(method, url, headers=self.headers)
        
        if response.status_code in (200, 201):
            return response.json()
        elif response.status_code == 204:
            return {}
        else:
            raise Exception(f"Failed to execute API call: {response.text}")
    
    def fetch_all(self, method: str, endpoint: str, params: dict = None) -> list:
        items = []
        page = 1
        while True:
            if params:
                params.update({'page': page})
            else:
                params = {'page': page, 'per_page': 100}  # Default per_page set to 100
            
            response = self.execute_api_call(method, endpoint, params=params)
            items.extend(response)  # Assuming response is a list of items
            
            # Break if there are no more items in the response
            if not response or len(response) < params['per_page']:
                break
            page += 1
        
        return items
    
    def get_org_repos(self, organisation: str) -> dict:
        return self.fetch_all("GET", f"orgs/{organisation}/repos")
    
    def get_user_repos(self, user: str) -> dict:
        return self.fetch_all("GET", f"users/{user}/repos")
    
    def list_webhooks(self, owner: str, repo: str) -> dict:
        return self.fetch_all("GET", f"repos/{owner}/{repo}/hooks")
    
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
        
        return self.execute_api_call("POST", f"repos/{owner}/{repo}/hooks", data=data)
    
    def delete_webhook(self, owner: str, repo: str, webhook_id: int) -> dict:
        logger.info(f"Deleting webhook {webhook_id} from {owner}/{repo}")

        return self.execute_api_call("DELETE", f"repos/{owner}/{repo}/hooks/{webhook_id}")