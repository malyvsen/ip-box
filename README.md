# IP Box

CLI toolkit for generatng IP-box documentation from a GitHub repository.

IP-box is a Polish tax break, frequently used by programmers engaged in R&D.

## Usage

Populate the `.env` file with the following variables:

- `GITHUB_TOKEN`: a GitHub personal access token which can read pull requests in the relevant repository
- `OPENAI_API_KEY`

The run:

```bash
pdm dev --help
```
