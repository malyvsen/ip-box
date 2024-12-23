from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from github.PullRequest import PullRequest as GithubPullRequest
from github.Repository import Repository
from tqdm import tqdm


@dataclass(frozen=True)
class PullRequest(ABC):
    title: str
    number: int
    url: str
    author: str
    created_at: datetime
    description: str | None

    @staticmethod
    async def from_repository(
        repo: Repository,
    ) -> list["OpenPullRequest | ClosedPullRequest | MergedPullRequest"]:
        prs = repo.get_pulls(state="all")
        return [
            PullRequest.from_github_object(pr)
            for pr in tqdm(prs, desc="Listing PRs", total=prs.totalCount)
        ]

    @staticmethod
    def from_github_object(
        pr: GithubPullRequest,
    ) -> "OpenPullRequest | ClosedPullRequest | MergedPullRequest":
        description = pr.body if isinstance(pr.body, str) and len(pr.body) > 0 else None

        if pr.state == "open":
            return OpenPullRequest(
                title=pr.title,
                number=pr.number,
                url=pr.html_url,
                author=pr.user.login,
                created_at=pr.created_at,
                description=description,
            )

        if pr.merged_at is not None:
            return MergedPullRequest(
                title=pr.title,
                number=pr.number,
                url=pr.html_url,
                author=pr.user.login,
                created_at=pr.created_at,
                description=description,
                merged_at=pr.merged_at,
            )

        if pr.closed_at is not None:
            return ClosedPullRequest(
                title=pr.title,
                number=pr.number,
                url=pr.html_url,
                author=pr.user.login,
                created_at=pr.created_at,
                description=description,
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
