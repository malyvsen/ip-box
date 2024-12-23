from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from github.PullRequest import PullRequest as GithubPullRequest
from github.Repository import Repository
from tqdm import tqdm


@dataclass(frozen=True)
class PullRequest(ABC):
    title: str
    description: str | None
    created_at: datetime

    @staticmethod
    async def by_author(
        repo: Repository,
        author: str,
    ) -> list["OpenPullRequest | ClosedPullRequest | MergedPullRequest"]:
        prs = repo.get_pulls(state="all")
        return [
            PullRequest.from_github(pr)
            for pr in tqdm(prs, desc="Listing PRs", total=prs.totalCount)
            if pr.user.login == author
        ]

    @staticmethod
    def from_github(
        pr: GithubPullRequest,
    ) -> "OpenPullRequest | ClosedPullRequest | MergedPullRequest":
        if pr.state == "open":
            return OpenPullRequest(
                title=pr.title,
                description=pr.body if pr.body else None,
                created_at=pr.created_at,
            )

        if pr.merged_at is not None:
            return MergedPullRequest(
                title=pr.title,
                description=pr.body if pr.body else None,
                created_at=pr.created_at,
                merged_at=pr.merged_at,
            )

        if pr.closed_at is not None:
            return ClosedPullRequest(
                title=pr.title,
                description=pr.body if pr.body else None,
                created_at=pr.created_at,
                closed_at=pr.closed_at,
            )

        raise ValueError(f"Unknown pull request state for {pr.title}")


@dataclass(frozen=True)
class OpenPullRequest(PullRequest):
    pass


@dataclass(frozen=True)
class ClosedPullRequest(PullRequest):
    closed_at: datetime


@dataclass(frozen=True)
class MergedPullRequest(PullRequest):
    merged_at: datetime
