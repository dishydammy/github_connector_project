class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors."""
    pass

class ResourceNotFoundError(GitHubAPIError):
    """Exception raised when a requested resource is not found. Raised when the GitHub API returns a 404."""
    pass

class RateLimitExceededError(GitHubAPIError):
    """Exception raised when the GitHub API rate limit is exceeded. Raised when the GitHub API returns a 403 or 429 with rate limit info."""
    pass

class AuthenticationError(GitHubAPIError):
    """Exception raised for authentication failures. Raised when the GitHub API returns a 401."""
    pass