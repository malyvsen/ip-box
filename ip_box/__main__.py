from datetime import date

import asyncclick as click

from .git_username import git_username
from .github_client import github_client
from .pull_request import MergedPullRequest, PullRequest
from .write_project_description import write_project_description


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
async def main(repo: str, author: str, year: int):
    repo_object = github_client.get_repo(repo)
    all_prs = await PullRequest.from_repository(repo_object)
    fitting_prs = [
        pr
        for pr in all_prs
        if isinstance(pr, MergedPullRequest)
        if pr.merged_at.year == year
        if pr.author == author
    ]
    grouped_by_month = MergedPullRequest.group_by_month(fitting_prs)
    descriptions_by_month = {
        month: await write_project_description(prs)
        for month, prs in grouped_by_month.items()
        if len(prs) > 0
    }
    print(
        "\n\n".join(
            f"{month}.{year}:\n{description}"
            for month, description in descriptions_by_month.items()
        )
    )


main()
