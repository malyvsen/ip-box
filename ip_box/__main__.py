from datetime import date

import asyncclick as click

from .git_username import git_username
from .github_client import github_client
from .pull_request import MergedPullRequest, PullRequest


@click.command()
@click.argument("repo", required=True)
@click.option(
    "--author",
    help="GitHub username of the author of the pull requests",
    default=git_username,
)
@click.option(
    "--year",
    type=click.IntRange(2000, date.today().year),
    help="Only include PRs merged in this year",
    default=date.today().year,
)
@click.option(
    "--month",
    type=click.IntRange(1, 12),
    help="Only include PRs merged in this month",
    default=date.today().month,
)
async def main(repo: str, author: str, year: int, month: int):
    repo_object = github_client.get_repo(repo)
    all_prs = await PullRequest.from_repository(repo_object)
    fitting_prs = [
        pr
        for pr in all_prs
        if isinstance(pr, MergedPullRequest)
        if pr.merged_at.year == year and pr.merged_at.month == month
        if pr.author == author
    ]
    print("\n\n".join(f"{pr.title}\n{pr.description}" for pr in fitting_prs))


main()
