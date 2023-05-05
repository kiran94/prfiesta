import logging
from datetime import datetime

import click
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

from prfiesta import SPINNER_STYLE
from prfiesta.collectors.github import GitHubCollector
from prfiesta.environment import GitHubEnvironment
from prfiesta.output import output_frame

logger = logging.getLogger(__name__)

github_environment = GitHubEnvironment()


@click.command()
@click.option('-u', '--users', required=True, multiple=True, help='The GitHub Users to search for. Can be multiple (space delimited)')
@click.option('-t', '--token', help='The Authentication token to use')
@click.option('-x', '--url', help='The URL of the Git provider to use')
@click.option('-o', '--output', default=None, help='The output location')
@click.option('-ot', '--output_type', type=click.Choice(['csv', 'parquet']), default='csv', help='The output format')
@click.option('--after', type=click.DateTime(formats=['%Y-%m-%d']), help='Only search for pull requests after this date e.g 2023-01-01')
@click.option('--before', type=click.DateTime(formats=['%Y-%m-%d']), help='Only search for pull requests before this date e.g 2023-04-30')
def main(**kwargs) -> None:

    users: tuple[str] = kwargs.get('users')
    token: str = kwargs.get('token') or github_environment.get_token()
    url: str = kwargs.get('url') or github_environment.get_url()
    output: str = kwargs.get('output')
    output_type: str = kwargs.get('output_type')
    before: datetime = kwargs.get('before')
    after: datetime = kwargs.get('after')

    logger.info('[bold green]Pull Request Fiesta 🦜🥳')

    spinner = Spinner('dots', text=Text('Loading', style=SPINNER_STYLE))

    with Live(spinner, refresh_per_second=20, transient=True):

        collector = GitHubCollector(token=token, url=url, spinner=spinner)
        pr_frame = collector.collect(users, after=after, before=before)

        logger.info('Found [bold green]%s[/bold green] pull requests!', pr_frame.shape[0])

        if not pr_frame.empty:
            output_frame(pr_frame, output_type, spinner=spinner, output_name=output)

if __name__ == '__main__':  # pragma: nocover
    main()