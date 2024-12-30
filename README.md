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
pdm ip-box list-prs org/repo  # lists all PRs in the repository, writes to prs.pickle
pdm ip-box generate  # generates the documentation, writes to ip_box.csv
```

You can optionally pass `--author` and `--year` to `generate` - they have sensible defaults, though.

## Warranty

It's AI generated output, and I'm not a lawyer. Use at your own risk, I cannot give any warranty.

That said, I _did_ base this on my conversations with a lawyer, a tax advisor, and an accountant.

## Development

Use `pdm check` to ensure code quality.
