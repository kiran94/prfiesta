from datetime import datetime, timezone
from typing import Dict
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from prfiesta.analysis.view import view_pull_requests

_now = datetime.now(timezone.utc)


@pytest.mark.parametrize(('data', 'options', 'expected'), [
    pytest.param(
        pd.DataFrame(data =
        {
            'number': [1, 2],
            'title': ['title', 'title2'],
            'repository_name': ['repository', 'repository'],
            'updated_at': [datetime.now(timezone.utc), datetime.now(timezone.utc)],
            'html_url': ['url1', 'url2'],
         }),
        {'as_frame': True},
        pd.DataFrame(data={
            'number': [1, 2],
            'title': ['<a href="url1">title</a>', '<a href="url2">title2</a>'],
            'repository_name': ['repository']*2,
            'updated_at': ['just now']*2,
        }),
        id='as_frame_with_defaults',
    ),
    pytest.param(
        pd.DataFrame(data =
        {
            'number': [1, 2],
            'title': ['title', 'title2'],
            'repository_name': ['repository', 'repository'],
            'updated_at': [_now, _now],
            'html_url': ['url1', 'url2'],
         }),
        {'as_frame': True, 'relative_dates': False},
        pd.DataFrame(data={
            'number': [1, 2],
            'title': ['<a href="url1">title</a>', '<a href="url2">title2</a>'],
            'repository_name': ['repository']*2,
            'updated_at': [_now, _now],
        }),
        id='as_frame_with_no_relative_dates',
    ),
    pytest.param(
        pd.DataFrame(data =
        {
            'number': [1, 2],
            'title': ['title', 'title2'],
            'repository_name': ['repository', 'repository'],
            'updated_at': [datetime.now(timezone.utc), datetime.now(timezone.utc)],
            'html_url': ['url1', 'url2'],
         }),
        {'as_frame': True, 'head': 1},
        pd.DataFrame(data={
            'number': [1],
            'title': ['<a href="url1">title</a>'],
            'repository_name': ['repository'],
            'updated_at': ['just now'],
        }),
        id='as_frame_with_head',
    ),
    pytest.param(
        pd.DataFrame(data =
        {
            'number': [1, 2],
            'title': ['title', 'title2'],
            'repository_name': ['repository', 'repository'],
            'updated_at': [datetime.now(timezone.utc), datetime.now(timezone.utc)],
            'html_url': ['url1', 'url2'],
         }),
        {},
        pd.DataFrame(data={
            'number': [1, 2],
            'title': ['<a href="url1">title</a>', '<a href="url2">title2</a>'],
            'repository_name': ['repository']*2,
            'updated_at': ['just now']*2,
        }),
        id='html_default',
    ),
    pytest.param(
        pd.DataFrame(data =
        {
            'number': [1, 2],
            'title': ['title', 'title2'],
            'repository_name': ['repository', 'repository'],
            'updated_at': [datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z'), datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S%z')],
            'html_url': ['url1', 'url2'],
         }),
        {'as_frame': True},
        pd.DataFrame(data={
            'number': [1, 2],
            'title': ['<a href="url1">title</a>', '<a href="url2">title2</a>'],
            'repository_name': ['repository']*2,
            'updated_at': ['just now']*2,
        }),
        id='string_datetime',
    ),
])
@patch('prfiesta.analysis.view.HTML')
def test_view_pull_request(
        mock_html: Mock,
        data: pd.DataFrame,
        options: Dict,
        expected: pd.DataFrame) -> None:

    mock_html.return_value = 'DUMMY'

    result = view_pull_requests(data, **options)

    if 'as_frame' in options and options['as_frame']:
        pd.testing.assert_frame_equal(expected, result)
    else:
        assert mock_html.called
        assert result == mock_html.return_value
