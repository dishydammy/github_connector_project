from github_connector.client import GitHubClient
from github_connector.custom_exceptions import GitHubAPIError, ResourceNotFoundError

def main():
    print("---- Starting Github Connector Smoke Test ----\n")

    #Initialize Github Client
    client = GitHubClient()
    owner = "Paulooh007"
    repo = "drone-based-plant-monitoring-system"

    try:
        #Fetch repository details
        print(f"Fetching details for: {owner}/{repo}")
        details = client.get_repo_details(owner, repo)
        print("✅ Repository Details Retrieved Successfully:")
        print(f"   Name: {details.get('name')}")
        print(f"   Stars: {details.get('stargazers_count')}\n")
        
        #Get Latest Release
        print(f"Fetching latest release for: {owner}/{repo}")
        release = client.get_latest_release(owner, repo)
        print("✅ Latest Release Retrieved Successfully:")
        print(f".   Latest Version: {release.get('tag_name')}")
        print(f"   Published at: {release.get('published_at')}\n")
    
    except ResourceNotFoundError:
        print("❌ Error: The specified repository was not found.")
    except GitHubAPIError as e:
        print(f"❌ GitHub API Error occurred: {str(e)}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()