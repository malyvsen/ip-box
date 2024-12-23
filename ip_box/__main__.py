import asyncclick as click

from .git_username import git_username
from .github_client import github_client
from .pull_request import PullRequest


@click.command()
@click.argument("repo", required=True)
@click.option("--author", help="Author of the pull requests", default=git_username)
async def main(repo: str, author: str):
    repo_object = github_client.get_repo(repo)
    all_prs = await PullRequest.from_repository(repo_object)
    prs = [pr for pr in all_prs if pr.author == author]
    print("\n\n".join(f"{pr.title}\n{pr.description}" for pr in prs))


main()