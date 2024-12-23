from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from github.PullRequest import PullRequest as GithubPullRequest
from github.Repository import Repository
from tqdm import tqdm

from .month import Month


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

    @staticmethod
    def group_by_month(
        prs: Sequence["MergedPullRequest"],
    ) -> dict[Month, list["MergedPullRequest"]]:
        earliest = min(pr.merged_at for pr in prs)
        latest = max(pr.merged_at for pr in prs)
        months = Month.inclusive_range(
            Month.from_date(earliest), Month.from_date(latest)
        )

        result = {month: [] for month in months}
        for pr in prs:
            result[Month.from_date(pr.merged_at)].append(pr)

        return result
