import os
from typing import Sequence

from openai import AsyncClient

from ip_box.pull_request import PullRequest


async def write_description(pull_requests: Sequence[PullRequest]) -> str:
    """Generate a consolidated description of the work done in the PRs."""

    completion = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": (
                    INSTRUCTION
                    + "\n\n"
                    + "\n\n".join(format_pr(pr) for pr in pull_requests)
                    + "\n\n"
                    + EXAMPLE
                ),
            },
        ],
        temperature=0.1,
    )
    response = completion.choices[0].message.content
    assert response is not None
    return response


def format_pr(pr: PullRequest) -> str:
    pieces = {"url": pr.url, "title": pr.title}
    if pr.description is not None:
        pieces["description"] = pr.description

    xml = "\n".join(f"<{key}>{value}</{key}>" for key, value in pieces.items())
    return f"<pull-request>\n{xml}\n</pull-request>"


INSTRUCTION = """
<instruction>
Napisz zbiorczy opis prac wykonanych w następujących _pull requests_, odwołując się do nich po URL.
Nie wdawaj się w szczegóły techniczne ani nazwy kodowe. Wymieniaj kilka _pull requests_ w ramach jednego zdania/punktu, jeśli są powiązane. Szczególnie uwzględnij aspekt badawczo-rozwojowy.
Pisz rzeczownikami ("wdrożenie" zamiast "wdrożono").
Odpowiedz tylko opisem.
</instruction>
""".strip()

EXAMPLE = """
<example-output>
- Zwiększenie stabilności systemu wystosowującego zapytania do modeli językowych (https://github.com/beemployee/ml/pull/26).
- Stworzenie systemu ewaluacji klasyfikatora CV (https://github.com/beemployee/ml/pull/22) celem oceny i poprawy jego dokładności (https://github.com/beemployee/ml/pull/28).
- Wdrożenie automatycznego systemu sprawdzania kodu źródłowego (https://github.com/beemployee/ml/pull/27).
</example-output>
""".strip()


_api_key = os.getenv("OPENAI_API_KEY")
if _api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = AsyncClient(api_key=_api_key)
