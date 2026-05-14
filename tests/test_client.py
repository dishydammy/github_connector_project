import pytest
from unittest.mock import Mock, patch
from github_connector.client import GitHubClient
from github_connector.custom_exceptions import ResourceNotFoundError, RateLimitExceededError

@pytest.fixture
def client():
    return GitHubClient()

def test_get_repo_details_success(client):
    """Scenario: Github returns an okay 200 response with data"""
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "test-repo",
            "stargazers_count": 42
        }
        
        mock_request.return_value = mock_response

        result = client.get_repo_details("fake-owner", "fake-repo")
        assert result["name"] == "test-repo"
        assert result["stargazers_count"] == 42

        args, kwargs = mock_request.call_args
        assert args[1] == "https://api.github.com/repos/fake-owner/fake-repo"

def test_get_repo_details_not_found(client):
    """Scenario: Github returns a 404 Not Found response"""
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_request.return_value = mock_response

        with pytest.raises(ResourceNotFoundError):
            client.get_repo_details("ghost", "does-not-exist")

def test_retry_logic_eventual_success(client):
    """Scenario: API responds with 429 twice and then 200 on the 3rd try"""
    with patch('requests.request') as mock_request, patch('time.sleep') as mock_sleep:

        #create a bad response for 429
        bad_response = Mock()
        bad_response.status_code = 429

        #create a good response for 200
        good_response = Mock()
        good_response.status_code = 200
        good_response.json.return_value = {"status": "ok"}

        mock_request.side_effect = [bad_response, bad_response, good_response]

        result = client.get_repo_details("owner", "repo")

        assert result["status"] == "ok"
        assert mock_request.call_count == 3
        assert mock_sleep.call_count == 2

def test_retry_failure_max_exceeded(client):
    """Scenario: API fails for all retry attempts and then raises RateLimitExceededError"""
    with patch('requests.request') as mock_request, patch('time.sleep'):
        fail_response = Mock()
        fail_response.status_code = 429

        mock_request.return_value = fail_response
        
        with pytest.raises(RateLimitExceededError):
            client.get_repo_details("owner", "repo")
        
        assert mock_request.call_count == 4
