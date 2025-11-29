# GitHub Connector Project

A Python learning project that demonstrates how to interact with the GitHub API. Fetch repository details and latest releases with built-in error handling and retry logic.

## Features

- Fetch repository details
- Get latest release information
- Automatic retry with exponential backoff
- Custom exception handling
- Logging for debugging

## Prerequisites

- Python 3.10 or higher
- (Optional) A GitHub personal access token

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dishydammy/github_connector_project.git
   cd github_connector_project
   ```

2. **Install dependencies using Poetry**
   ```bash
   poetry install
   ```

3. **Set up environment variables (Optional)**
   
   Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   
   Add your GitHub token:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```
   
   > **Note**: The application works without a token, but you'll have stricter rate limits.

## Usage

Run the example:

```bash
poetry run python main.py
```

Or use it in your code:

```python
from github_connector.client import GitHubClient
from github_connector.custom_exceptions import ResourceNotFoundError

client = GitHubClient()

try:
    repo = client.get_repo_details("owner", "repo-name")
    print(f"Stars: {repo['stargazers_count']}")
    
    release = client.get_latest_release("owner", "repo-name")
    print(f"Latest: {release['tag_name']}")
except ResourceNotFoundError:
    print("Not found")
```

## Running Tests

```bash
poetry run -m pytest -v
```

## Project Structure

```
github_connector_project/
├── github_connector/
│   ├── client.py             # GitHub API client
│   └── custom_exceptions.py  # Custom exceptions
├── tests/
│   └── test_client.py        # Tests
├── main.py                    # Demo usage
└── pyproject.toml            # Dependencies
```

## Available Methods

- `get_repo_details(owner, repo)` - Get repository information
- `get_latest_release(owner, repo)` - Get latest release details

## Custom Exceptions

- `GitHubAPIError` - Base exception
- `ResourceNotFoundError` - Resource not found (404)
- `RateLimitExceededError` - Rate limit exceeded
- `AuthenticationError` - Authentication failed (401)
