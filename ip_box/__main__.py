from datetime import date
from pathlib import Path

import asyncclick as click

from .git_username import git_username
from .github_client import github_client
from .projects import generate_dataframe
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
    "--output",
    type=click.Path(exists=False, dir_okay=False, path_type=Path),
    help="Output file name",
    default="ip_box.csv",
)
async def main(repo: str, author: str, year: int, output: Path):
    repo_object = github_client.get_repo(repo)
    all_prs = await PullRequest.from_repository(repo_object)
    fitting_prs = [
        pr
        for pr in all_prs
        if isinstance(pr, MergedPullRequest)
        if pr.merged_at.year == year
        if pr.author == author
    ]
    dataframe = await generate_dataframe(fitting_prs)
    dataframe.to_csv(output)

    print(f"Write {len(dataframe)} rows to {output.as_posix()}")


main()
