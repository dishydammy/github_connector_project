import os
import time
import logging
import requests
from typing import Dict, Any

from dotenv import load_dotenv

from .custom_exceptions import GitHubAPIError, ResourceNotFoundError, RateLimitExceededError, AuthenticationError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GitHubClient:
    """"Client to interact with the Github API"""

    BASE_URL = "https://api.github.com"

    def __init__(self):
        load_dotenv()
        self.token = os.getenv("GITHUB_TOKEN")

        if not self.token:
            logger.warning("GITHUB_TOKEN not found in .env file. Rate Limits will be strictter.")
            self.headers = {"Accept": "application/vnd.github.v3+json"}
        else:
            self.headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
    
    def _make_request(self, method: str, endpoint: str) -> Dict[str, Any]:
        """Handles making requests to the GitHub API with error handling and rate limit management."""
        url = f"{self.BASE_URL}{endpoint}"
        retries = 0
        max_retries = 3

        while retries <= max_retries:
            try:
                logger.info(f"Requesting {method} {url} (Attempt {retries + 1})")

                response = requests.request(method, url, headers=self.headers)

                if response.status_code == 200:
                    return response.json()
                
                elif response.status_code == 404:
                    logger.error(f"Resource not found: {url}")
                    raise ResourceNotFoundError(f"Resource at {url} not found.")
                
                elif response.status_code in [403, 429]:
                    logger.warning(f"Rate limit exceeded. (Status {response.status_code}).")
                
                elif response.status_code == 401:
                    logger.error("Authentication failed.")
                    raise AuthenticationError("Invalid or missing GitHub token.")
                
                else:
                    raise GitHubAPIError(f"Unexpected error: {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error occurred: {str(e)}")
            
            # Exponential backoff before retrying
            if retries < max_retries:
                sleep_time = 2 ** retries
                logger.warning(f"Retrying in {sleep_time} seconds..")
                time.sleep(sleep_time)
                retries += 1
            else:
                logger.error("Max retries exceeded.")
                raise RateLimitExceededError("Exceeded maximum retries due to rate limiting or network issues.")
    
    def get_repo_details(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetches details of a specific repository."""
        endpoint = f"/repos/{owner}/{repo}"
        return self._make_request("GET", endpoint)
    
    def get_latest_release(self, owner: str, repo: str) -> Dict[str, Any]:
        """Feches the latest release of a specific repository."""
        endpoint = f"/repos/{owner}/{repo}/releases/latest"
        return self._make_request("GET", endpoint)
    

