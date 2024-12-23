import os

from github import Github

_github_token = os.getenv("GITHUB_TOKEN")
if _github_token is None:
    raise ValueError("GITHUB_TOKEN environment variable is not set")

github_client = Github(_github_token)
