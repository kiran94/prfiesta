# prfiesta 🦜🥳

[![main](https://github.com/kiran94/prfiesta/actions/workflows/main.yml/badge.svg)](https://github.com/kiran94/prfiesta/actions/workflows/main.yml) ![GitHub](https://img.shields.io/github/license/kiran94/prfiesta) [![PyPI](https://img.shields.io/pypi/v/prfiesta)](https://pypi.org/project/prfiesta/)

> Collect and Analyze Individual Contributor Pull Requests

`prfiesta` allows you to collect, analyze and celebrate pull requests made by an individual 🎉.

It can be used by engineers or managers to gain insights into all the great work the contributor has made over a specified period of time. A great use case of this tool is during a performance review process when you want to perform analysis on all the contributions made over the year.

[![asciicast](https://asciinema.org/a/587987.svg)](https://asciinema.org/a/587987)

## Install

```bash
python -m pip install prfiesta
```

Dependencies:

- Python 3.8+

## Usage

```bash
# Authenticate yourself
export GITHUB_TOKEN=... # or GITHUB_ENTERPRISE_TOKEN

# Get all pull requests for a user
prfiesta -u kiran94

# Get all pull requests for a user created after a date
prfiesta -u kiran94 --after 2023-01-01

# Get all pull requests for a user created between two dates
prfiesta -u kiran94 --after 2023-01-01 --before 2023-06-01

# Get all pull requests for a user updated after a date
prfiesta -u kiran94 --after 2023-01-01 --use-updated

# Get all pull requests with a custom output file name
prfiesta -u kiran94 --output my_pull_requests.csv

# Get all pull requests in parquet format with a custom file name
prfiesta -u kiran94 --output-type parquet --output my_pull_requests.parquet

# Get all pull requests and export to a duckdb database
prfiesta -u kiran94 --output-type duckdb --output mydatabase.duckdb

# Get all pull requests for more then one user
prfiesta -u kiran94 -u user2

# Get all pull requests and drop specific columns from the output
prfiesta -u kiran94 -dc events_url -dc comments_url -dc node_id

# Get all pull requests where the user was involved (as opposed to just authored)
prfiesta -u kiran94 --use-involves

# Get all pull requests where the user reviewed it rather then being the author
prfiesta -u charliermarsh --after 2023-05-01 --use-reviewed-by

# Get all pull requests where the user was requested a review rather then being the author
prfiesta -u charliermarsh --after 2023-05-01 --use-review-requested

# Get help
prfiesta --help

# Show the current version
prfiesta --version
```

You can also leverage `prfiesta` directly in your own application:

```python
import pandas as pd

from datetime import datetime
from prfiesta.collectors.github import GitHubCollector

github = GitHubCollector()
frame: pd.DataFrame = github.collect('kiran94', 'user2', after=datetime(2023, 1, 1))

print(frame)
```

### Output

You can control the output type using the `--output-type` option. Supported options:

- `csv` (default)
- `parquet`
- [`duckdb`](https://duckdb.org/)

You can also customize the output file name using the `--output` option. When using `duckdb`, this argument is the duckdb database that we should export into. You can see an example of a duckdb workflow [here](https://github.com/kiran94/prfiesta/blob/main/notebooks/misc/duckdb_integration.ipynb).

### User Filter

By default, `prfiesta` will take the users provided in the `--user` option and search the Git provider for any pull requests that the user **authored**. Within more collaborative environments, this may not be what you want as you may want to also gain some visibility into all secondary contributions a user made (e.g commenting on others pull requests).

*The options listed here are mutually exclusive.*

#### User Involvement

`prfiesta` exposes the `--use-involves` flag which will search for pull requests that were:

- Created by a certain user
- Assigned to that user
- Mention that user
- commented on by that user

Learn more about `involves` [here](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-a-user-thats-involved-in-an-issue-or-pull-request).

#### User Reviewed

`prfiesta` exposes a `--use-reviewed-by` flag which will collect pull requests where the user *has reviewed* other's pull requests.

Learn more about searching review requests [here](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer)

#### User Requested Review

`prfiesta` exposes a `--use-review-requested` flag which will collect pull requests where the user was *requested* a review from other collaborators.

Learn more about searching review requests [here](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer)

### Date Filter

When using the `--after` and `--before` date filters, by default `prfiesta` will use the `created` date dimension with these filters on the Git provider (e.g GitHub). This may not fit your use case and you may want to filter on when a pull request was `updated` instead. To do this you can use the `--use-updated` flag.

Learn more about date filters [here](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-when-an-issue-or-pull-request-was-created-or-last-updated).

## Analysis

`prfiesta` ships with built in plots to help analyze your pull request data. These serve as a starting point in your analysis. See more information on the build in plots and views [here](https://github.com/kiran94/prfiesta/blob/main/docs/analysis.md).

## Using GitHub Enterprise

If you trying to fetch data from a [GitHub Enterprise](https://docs.github.com/en/enterprise-cloud@latest/rest/enterprise-admin?apiVersion=2022-11-28) server, then much of the same functionality should work the same. You just need to make sure that:

- `GH_HOST` is set to your enterprise instance's API URL. Reach out to your internal GitHub team if you are not sure what this should be.
- `GITHUB_ENTERPRISE_TOKEN` a [personal access token](https://docs.github.com/en/enterprise-cloud@latest/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) generated on your GitHub Enterprise instance.

## GitHub Rate Limiting

Depending on your input parameters, you may end up in a situation where you are being [Rate Limited](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limiting) by the GitHub API.

See this [Notebook](https://github.com/kiran94/prfiesta/blob/main/notebooks/misc/rate_limit.ipynb) on a way to handle this.

## Environment Variables

| Variable                  | Description                                                                                                                                  | Default                  |
| ---------------           | ---------------                                                                                                                              | ------                   |
| `GITHUB_TOKEN`            | The Github [`Token`](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) to use |                          |
| `GITHUB_ENTERPRISE_TOKEN` | Takes precedence over `GITHUB_TOKEN` when set                                                                                                |                          |
| `GH_HOST`                 | The Github Host to communicate with (Override this with your company's GitHub Enterprise server if needed)                                   | `https://api.github.com` |
| `LOGGING_LEVEL`           | The [Logging Level](https://docs.python.org/3/library/logging.html#logging-levels) to use                                                    | `INFO`                   |
| `LOGGING_FORMAT`          | The [Logging Format](https://docs.python.org/3/library/logging.html#logrecord-attributes) to use                                             | `%(message)s`            |
| `SPINNER_STYLE`           | The [Spinner Style](https://rich.readthedocs.io/en/stable/reference/spinner.html)  to use                                                    | `blue`                   |

## Developer Setup

Assuming you have cloned the repository and are at the root of the repository in your terminal.

```bash
poetry shell
poetry install
poetry build
```

This should leave you in a state where you have the virtual environment sourced, all dependencies are installed and `prfiesta` is installed locally.

You can then leverage the various commands in the [makefile](https://github.com/kiran94/prfiesta/blob/main/makefile) for development tasks:

```bash
# Run all unit tests
make test

# Produce code coverage reports
make coverage

# Code linting
make lint
```

Optionally you can also install [pre-commit](https://github.com/pre-commit/pre-commit) to run some sanity checks before your commits.

```bash
# Install it into your git hooks (one time setup)
# from this point onwards, any commits will run pre-commit checks
precommit_install

# If you want to run all checks on all files without comitting.
precommit_run
```

### Creating Prereleases

When you create a pull request on this repository, various CI checks are run, towards the end of those checks there is a `release` job.

Usually when running under `main`, this job is responsible for publishing new versions to pypi. However when running under a pull request, this will create a special prerelease package specific to that pull request.

The versioning of this package follows [PEP-440](https://peps.python.org/pep-0440/#pre-releases) and will look something like this:

```
0.8.1b125
```

Where
- `0.8.1` = The bumped version of what is currently within the `pyproject.toml` of that pull request. We don't attempt to do any analysis to figure out if we should be bumping with a higher serverity in this context.
- `b` = Beta; Indicates to pypi that this is a prerelease package.
- `125` = The `github.run_number` from [GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/contexts#github-context).

An example prerelease package looks like this: https://pypi.org/project/prfiesta/0.8.1b125/

Downstream users can then do a full end to end test with the prerelease package before the change is merged into `main`. This will automatically be posted into the pull request [example](https://github.com/kiran94/prfiesta/pull/36#issuecomment-1564909558).

You can find the full version history of package [here](https://pypi.org/project/prfiesta/#history)
