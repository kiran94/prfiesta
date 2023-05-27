import logging
from datetime import datetime
from typing import List, Optional, Tuple

import pandas as pd
from github import Github
from github.GithubException import RateLimitExceededException
from rich.spinner import Spinner

from prfiesta.environment import GitHubEnvironment
from prfiesta.spinner import update_spinner

logger = logging.getLogger(__name__)


class GitHubCollector:

    def __init__(self, **kwargs) -> None:

        environment = GitHubEnvironment()
        token = kwargs.get('token') or environment.get_token()
        self._url = kwargs.get('url') or environment.get_url()

        self._github = Github(token, base_url=self._url)
        self._spinner: Spinner = kwargs.get('spinner')

        self._sort_column = ['updated_at']
        self._drop_columns = kwargs.get('drop_columns') or ['node_id', 'performed_via_github_app']

        self._move_to_end_columns = [
            'url',
            'repository_url',
            'html_url',
            'timeline_url',
            'labels_url',
            'comments_url',
            'events_url',
        ]
        self._datetime_columns = [
            'created_at',
            'updated_at',
            'closed_at',
        ]


    def collect(
            self,
            *users: Tuple[str],
            after: Optional[datetime] = None,
            before: Optional[datetime] = None,
            use_updated: Optional[bool] = False,
            use_involves: Optional[bool] = False,
            use_reviewed_by: Optional[bool] = False,
            use_review_requested: Optional[bool] = False,
        ) -> pd.DataFrame:

        query = self._construct_query(users, after, before, use_updated, use_involves, use_reviewed_by, use_review_requested)

        update_spinner(f'Searching {self._url} with[bold blue] {query}', self._spinner,  logger)

        pull_request_data = None
        try:
            pulls = self._github.search_issues(query=query)

            pull_request_data: list[dict] = []
            for pr in pulls:
                pull_request_data.append(pr.__dict__['_rawData'])

        except RateLimitExceededException as e:
            logger.warning('🙇 You were rate limited by the GitHub API, try requesting less data.')
            logger.debug(e)
            return pd.DataFrame()

        if not pull_request_data:
            logger.warning('Did not find any results for this search criteria!')
            return pd.DataFrame()

        update_spinner('Post Processing', self._spinner, logger)
        pr_frame = pd.json_normalize(pull_request_data)

        pr_frame = pr_frame.drop(columns=self._drop_columns, errors='ignore')
        pr_frame = pr_frame.sort_values(by=self._sort_column, ascending=False)
        pr_frame = self._parse_datetime_columns(pr_frame)
        pr_frame['repository_name'] = pr_frame['repository_url'].str.extract(r'(.*)\/repos\/(?P<repository_name>(.*))')['repository_name']
        pr_frame = self._move_column_to_end(pr_frame)

        return pr_frame


    @staticmethod
    def _construct_query(
            users: List[str],
            after: Optional[datetime] = None,
            before: Optional[datetime] = None,
            use_updated: Optional[bool] = False,
            use_involves: Optional[bool] = False,
            use_reviewed_by: Optional[bool] = False,
            use_review_requested: Optional[bool] = False,
        ) -> str:
        """
        Constructs a GitHub Search Query
        that returns pull requests made by the passed users and options.

        Examples
        --------
            type:pr author:user1
            type:pr author:user2 created:<=2021-01-01
            type:pr author:user1 author:user2 created:2021-01-01..2021-03-01
            type:pr author:user2 updated:>=2021-01-01
            type:pr involves:user2
            type:pr reviewed-by:user1
            type:pr review-requested:user1

        All dates are inclusive.
        See GitHub Docs for full options https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests
        """
        query: List[str] = []
        query.append('type:pr')

        author_filter = 'author'
        if use_involves:
            author_filter = 'involves'
        elif use_reviewed_by:
            author_filter = 'reviewed-by'
        elif use_review_requested:
            author_filter = 'review-requested'

        logger.debug('using author filter %s', author_filter)

        for u in users:
            query.append(f'{author_filter}:{u}')

        time_filter = 'created'
        if use_updated:
            time_filter = 'updated'

        logger.debug('using time filter %s', time_filter)

        if before and after:
            query.append(f"{time_filter}:{after.strftime('%Y-%m-%d')}..{before.strftime('%Y-%m-%d')}")
        elif before:
            query.append(f"{time_filter}:<={before.strftime('%Y-%m-%d')}")
        elif after:
            query.append(f"{time_filter}:>={after.strftime('%Y-%m-%d')}")

        return ' '.join(query)

    def _move_column_to_end(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self._move_to_end_columns:
            try:
                df.insert(len(df.columns)-1, col, df.pop(col))
                df.drop(columns=col)
            except KeyError:
                # This can happen if the user provides a custom _drop_columns which
                # removes the column before we can move it to the end
                logger.debug('Attempted to move column %s but it did not exist', col)

        return df

    def _parse_datetime_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self._datetime_columns:
            df[col] = pd.to_datetime(df[col], errors='ignore')
        return df



if __name__ == '__main__':  # pragma: nocover
    g = GitHubCollector()
    logger.info(g._construct_query(['kiran94', 'hello'], datetime(2021, 1, 1), datetime(2021, 3, 1)))
