# prfiesta 🦜🥳

[![main](https://github.com/kiran94/prfiesta/actions/workflows/main.yml/badge.svg)](https://github.com/kiran94/prfiesta/actions/workflows/main.yml) ![GitHub](https://img.shields.io/github/license/kiran94/prfiesta)

> Collect and Analyze Individual Contributor Pull Requests

`prfiesta` allows you to collect, analyze and celebrate pull requests made by an individual 🎉.

It can be used by engineers or managers to gain insights into all the great work the contributor has made over a specified period of time. A great use case of this tool is during a performance review process when you want to perform analysis on all the contributions made over the year.

## Install

```
TODO
```

Dependencies:

- Python 3.8+

## Usage

```bash
# Authenticate yourself
export GITHUB_TOKEN=... # or GITHUB_ENTERPRISE_TOKEN

# Get all pull requests for a user
prfiesta -u kiran94

# Get all pull requests for a user a date
prfiesta -u kiran94 --after 2023-01-01

# Get all pull requests for a user between two dates
prfiesta -u kiran94 --after 2023-01-01 --before 2023-06-01

# Get all pull requests with a custom output file name
prfiesta -u kiran94 --output my_pull_requests.csv

# Get all pull requests in parquet format with a custom file name
prfiesta -u kiran94 --output_type parquet --output my_pull_requests.parquet

# Get all pull requests for more then one user
prfiesta -u kiran94 -u user2

# Get help
prfiesta --help
```

You can also leverage `prfiesta` directly in your own application:

```python
from datetime import datetime

import pandas as pd

from prfiesta.collectors.github import GitHubCollector

github = GitHubCollector()
frame: pd.DataFrame = github.collect('kiran94', 'user2', after=datetime(2023, 1, 1))

print(frame)
```

### Output

You can control the output type using the `--output_type` option. Supported options:

- `csv` (default)
- `parquet`

You can also customize the output file name using the `--output` option.

## Analysis

`prfiesta` ships with built in plots to help analyze your pull request data. These serve as a starting point in your analysis. See more information on the build in plots and views [here](./docs/analysis.md).

### Using GitHub Enterprise

TODO

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

You can then leverage the various commands in the [makefile](./makefile) for development tasks:

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