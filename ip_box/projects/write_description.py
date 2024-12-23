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
    pieces = {
        "number": pr.number,
        "url": pr.url,
        "title": pr.title,
    }
    if pr.description is not None:
        pieces["description"] = pr.description

    xml = "\n".join(f"<{key}>{value}</{key}>" for key, value in pieces.items())
    return f"<pull-request>\n{xml}\n</pull-request>"


INSTRUCTION = """
<polecenie>
Napisz zbiorczy opis prac wykonanych w następujących _pull requests_. Odpowiedz tylko opisem. Przy tworzeniu opisu odwołuj się do _pull requests_ według liczb i URL.
</polecenie>
""".strip()

EXAMPLE = """
<przykład>
Wdrożenie nowych widoków do beemployee.pl oraz rozbudowa funkcjonalności systemu (PR [#24](https://github.com/beemployee/webapp/pull/24)).
Wyświetlanie zamówień i wydarzeń na Kokpicie w aplikacji iOS (PR [#29](https://github.com/beemployee/ios/pull/29), [#30](https://github.com/beemployee/ios/pull/30)).
</przykład>
""".strip()


_api_key = os.getenv("OPENAI_API_KEY")
if _api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = AsyncClient(api_key=_api_key)
