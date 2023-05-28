import logging
from datetime import datetime

import click
import cloup
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

from prfiesta import SPINNER_STYLE, __version__
from prfiesta.collectors.github import GitHubCollector
from prfiesta.environment import GitHubEnvironment
from prfiesta.output import output_frame

logger = logging.getLogger(__name__)

github_environment = GitHubEnvironment()

@cloup.command()
@cloup.option_group(
    'general options',
    cloup.option('-u', '--users', required=True, multiple=True, help='The GitHub Users to search for. Can be multiple'),
)
@cloup.option_group(
    'date filter options',
    cloup.option('-a', '--after', type=click.DateTime(formats=['%Y-%m-%d']), help='Only search for pull requests after this date e.g 2023-01-01'),
    cloup.option('-b', '--before', type=click.DateTime(formats=['%Y-%m-%d']), help='Only search for pull requests before this date e.g 2023-04-30'),
    cloup.option('-d', '--use-updated', is_flag=True, default=False, help='filter on when the pr was last updated rather then created'),
)
@cloup.option_group(
    'user filter options',
    cloup.option('-i', '--use-involves', is_flag=True, default=False, help='collect prs where the users are the author or assignee or mentioned or commented'),
    cloup.option('-r', '--use-reviewed-by', is_flag=True, default=False, help='collect prs where the users reviewed them'),
    cloup.option('-rr', '--use-review-requested', is_flag=True, default=False, help='collect prs where the users were requested a review'),
    constraint=cloup.constraints.mutually_exclusive,
    help='Collect alternative details for the users. If omitted then just collect the prs that a user has authored.',
)
@cloup.option_group(
    'output options',
    cloup.option('-o', '--output', default=None, help='The output location'),
    cloup.option(
        '-ot', '--output-type', type=click.Choice(['csv', 'parquet', 'duckdb']), default='csv', show_default=True, show_choices=True, help='The output format'),
    cloup.option('-dc', '--drop-columns', multiple=True, help='Drop columns from the output dataframe'),
)
@cloup.option_group(
    'authentication options',
    cloup.option('-x', '--url', help='The URL of the Git provider to use'),
    cloup.option('-t', '--token', help='The Authentication token to use'),
)
@cloup.version_option(__version__)
def main(**kwargs) -> None:

    users: tuple[str] = kwargs.get('users')
    token: str = kwargs.get('token') or github_environment.get_token()
    url: str = kwargs.get('url') or github_environment.get_url()
    output: str = kwargs.get('output')
    output_type: str = kwargs.get('output_type')
    before: datetime = kwargs.get('before')
    after: datetime = kwargs.get('after')
    drop_columns: list[str] = list(kwargs.get('drop_columns'))
    use_updated: bool = kwargs.get('use_updated')
    use_involves: bool = kwargs.get('use_involves')
    use_reviewed_by: bool = kwargs.get('use_reviewed_by')
    use_review_requested: bool = kwargs.get('use_review_requested')

    logger.info('[bold green]PR Fiesta 🦜🥳')

    spinner = Spinner('dots', text=Text('Loading', style=SPINNER_STYLE))

    with Live(spinner, refresh_per_second=20, transient=True):

        collector = GitHubCollector(token=token, url=url, spinner=spinner, drop_columns=drop_columns)
        pr_frame = collector.collect(
            *users,
            after=after,
            before=before,
            use_updated=use_updated,
            use_involves=use_involves,
            use_reviewed_by=use_reviewed_by,
            use_review_requested=use_review_requested)

        if not pr_frame.empty:
            logger.info('Found [bold green]%s[/bold green] pull requests!', pr_frame.shape[0])

            output_frame(pr_frame, output_type, spinner=spinner, output_name=output)
            logger.info('Time to analyze 🔎 See https://github.com/kiran94/prfiesta/blob/main/docs/analysis.md for some inspiration!')

if __name__ == '__main__':  # pragma: nocover
    main()
