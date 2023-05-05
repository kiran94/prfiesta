import logging
from datetime import datetime
from typing import List, Optional

import pandas as pd
from github import Github
from rich.spinner import Spinner

from prfiesta import SPINNER_STYLE
from prfiesta.environment import GitHubEnvironment

logger = logging.getLogger(__name__)


class GitHubCollector:

    def __init__(self, **kwargs) -> None:

        environment = GitHubEnvironment()
        token = kwargs.get('token') or environment.get_token()
        self._url = kwargs.get('url') or environment.get_url()

        self._github = Github(token, base_url=self._url)
        self._spinner: Spinner = kwargs.get('spinner')

        self._sort_column = ['updated_at']
        self._drop_columns = [
            'labels_url',
            'comments_url',
            'events_url',
            'node_id',
            'performed_via_github_app',
            'active_lock_reason',
        ]
        self._move_to_end_columns = [
            'url',
            'repository_url',
            'html_url',
            'timeline_url',
        ]
        self._datetime_columns = [
            'created_at',
            'updated_at',
            'closed_at',
            'milestone.created_at',
            'milestone.updated_at',
            'milestone.due_on',
            'milestone.closed_at',
        ]


    def collect(self, users: List[str], after: Optional[datetime] = None, before: Optional[datetime] = None) -> pd.DataFrame:

        query = self._construct_query(users, after, before)

        self._update_spinner(f'Searching {self._url} with[bold blue] {query}')
        pulls = self._github.search_issues(query=query)

        pull_request_data: list[dict] = []
        for pr in pulls:
            pull_request_data.append(pr.__dict__['_rawData'])

        if not pull_request_data:
            logger.warning('Did not find any results for this search criteria!')
            return pd.DataFrame()

        self._update_spinner('Post Processing')
        pr_frame = pd.json_normalize(pull_request_data)

        pr_frame = pr_frame.drop(columns=self._drop_columns, errors='ignore')
        pr_frame = pr_frame.sort_values(by=self._sort_column, ascending=False)
        pr_frame = self._parse_datetime_columns(pr_frame)
        pr_frame['repository_name'] = pr_frame['repository_url'].str.extract(r'(.*)\/repos\/(?P<repository_name>(.*))')['repository_name']
        pr_frame = self._move_column_to_end(pr_frame)

        return pr_frame


    @staticmethod
    def _construct_query(users: list[str], after: datetime | None= None, before: datetime | None = None) -> str:
        """
        Constructs a GitHub Search Query
        that returns pull requests made by the passed users.

        Examples
        --------
            type:pr author:user1
            type:pr author:user2 updated:<=2021-01-01
            type:pr author:user1 author:user2 updated:2021-01-01..2021-03-01

        All dates are inclusive.
        See GitHub Docs for full optons https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests
        """
        query: list[str] = []

        query.append('type:pr')

        for u in users:
            query.append('author:' + u)

        if before and after:
            query.append(f"updated:{after.strftime('%Y-%m-%d')}..{before.strftime('%Y-%m-%d')}")
        elif before:
            query.append(f"updated:<={before.strftime('%Y-%m-%d')}")
        elif after:
            query.append(f"updated:>={after.strftime('%Y-%m-%d')}")

        return ' '.join(query)

    def _move_column_to_end(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self._move_to_end_columns:
            df.insert(len(df.columns)-1, col, df.pop(col))
            df.drop(columns=col)

        return df

    def _parse_datetime_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self._datetime_columns:
            df[col] = pd.to_datetime(df[col], errors='ignore')
        return df


    def _update_spinner(self, message: str, style: str=SPINNER_STYLE) -> None:
        if self._spinner:
            self._spinner.update(text=message, style=style)



if __name__ == '__main__':  # pragma: nocover
    g = GitHubCollector()
    logger.info(g._construct_query(['kiran94', 'hello'], datetime(2021, 1, 1), datetime(2021, 3, 1)))
