from typing import Sequence

import pandas as pd
from tqdm.asyncio import tqdm

from ip_box.pull_request import MergedPullRequest

from .write_description import write_description


async def generate_dataframe(
    pull_requests: Sequence[MergedPullRequest],
) -> pd.DataFrame:
    """Generate the IP-box documentation dataframe from the pull requests."""

    grouped = MergedPullRequest.group_by_month(pull_requests)
    present_months = [month for month, prs in grouped.items() if len(prs) > 0]
    descriptions: list[str] = await tqdm.gather(
        *[write_description(grouped[month]) for month in present_months],
        desc="Generating descriptions",
    )
    nans = [float("nan") for _ in range(len(present_months))]
    empty = ["" for _ in range(len(present_months))]
    return pd.DataFrame(
        {
            "Liczba porządkowa": list(range(1, len(present_months) + 1)),
            "Rok": [month.year for month in present_months],
            "Miesiąc": [month.polish_name.title() for month in present_months],
            "Data rozpoczęcia": [month.first_day for month in present_months],
            "Data zakończenia": [month.last_day for month in present_months],
            "Opis prac": descriptions,
            "Czas prac (w godzinach)": nans,
            "Przychód z prac B+R (w PLN)": nans,
            "Opis kosztów związanych z pracami B+R": empty,
            "Suma kosztów (w PLN)": nans,
        }
    )
