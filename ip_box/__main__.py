import pickle
from datetime import date
from pathlib import Path

import asyncclick as click

from .git_username import git_username
from .github_client import github_client
from .projects import generate_dataframe
from .pull_request import MergedPullRequest, PullRequest

default_prs_file = Path("prs.pickle")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("repo", required=True)
@click.argument(
    "output",
    type=click.Path(exists=False, dir_okay=False, path_type=Path),
    default=default_prs_file,
)
async def list_prs(repo: str, output: Path):
    repo_object = github_client.get_repo(repo)
    all_prs = await PullRequest.from_repository(repo_object)
    pickle.dump(all_prs, output.open("wb"))


@cli.command()
@click.argument(
    "input",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=default_prs_file,
)
@click.argument(
    "output",
    type=click.Path(exists=False, dir_okay=False, path_type=Path),
    default=Path("ip_box.csv"),
)
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
async def generate(input: Path, output: Path, author: str, year: int):
    with input.open("rb") as file:
        all_prs = pickle.load(file)

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


cli()
