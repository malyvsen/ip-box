# IP Box

CLI toolkit for generatng IP-box documentation from the PR history of a GitHub repository.

IP-box is a Polish tax break, frequently used by programmers engaged in R&D.

## Usage

This project uses the [PDM](https://pdm-project.org/latest/) package manager. Make sure to install it.

Populate the `.env` file with the following variables:

- `GITHUB_TOKEN`: a GitHub personal access token which can read pull requests in the relevant repository
- `OPENAI_API_KEY`

The run:

```bash
pdm dev list-prs org/repo  # lists all PRs in the repository, writes to prs.pickle
pdm dev generate --author your-github-username --year 2024  # generates the documentation, writes to ip_box.csv
```

## Development

Use `pdm check` to ensure code quality.
