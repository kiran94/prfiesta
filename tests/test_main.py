import os
from datetime import datetime
from unittest.mock import ANY, Mock, call, patch

import pandas as pd
import pytest
from click.testing import CliRunner

from prfiesta.__main__ import main

FAILURE_CODE = 2


def test_main_missing_users() -> None:
    runner = CliRunner()
    result = runner.invoke(main, [''])

    assert "Missing option '-u' / '--users'" in result.output
    assert result.exit_code == FAILURE_CODE

@pytest.mark.parametrize(('params', 'expected_collect_params', 'collect_response', 'expected_output_type'), [

    pytest.param
    (
        ['--users', 'test_user'],
        [call(('test_user',), after=None, before=None)],
        pd.DataFrame(),
        'csv',
        id='user_provided',
    ),
    pytest.param
    (
        ['--users', 'test_user', '--after', '2020-01-01'],
        [call(('test_user',), after=datetime(2020, 1, 1), before=None)],
        pd.DataFrame(),
        'csv',
        id='with_after',
    ),
    pytest.param
    (
        ['--users', 'test_user', '--before', '2020-01-01'],
        [call(('test_user',), before=datetime(2020, 1, 1), after=None)],
        pd.DataFrame(),
        'csv',
        id='with_before',
    ),
    pytest.param
    (
        ['--users', 'test_user', '--before', '2020-01-01', '--after', '2009-01-01'],
        [call(('test_user',), before=datetime(2020, 1, 1), after=datetime(2009, 1, 1))],
        pd.DataFrame(),
        'csv',
        id='with_before_and_after',
    ),
    pytest.param
    (
        ['--users', 'test_user'],
        [call(('test_user',), after=None, before=None)],
        pd.DataFrame(
                data=[(1, 2, 3)],
                columns=['col1', 'col2', 'col3'],
        ),
        'csv',
        id='with_collected_responses',
    ),
    pytest.param
    (
        ['--users', 'test_user', '--output_type', 'parquet'],
        [call(('test_user',), after=None, before=None)],
        pd.DataFrame(
                data=[(1, 2, 3)],
                columns=['col1', 'col2', 'col3'],
        ),
        'parquet',
        id='with_parquet',
    ),
])
@patch('prfiesta.__main__.Spinner')
@patch('prfiesta.__main__.Live')
@patch('prfiesta.__main__.GitHubCollector')
@patch('prfiesta.__main__.output_frame')
@patch.dict(os.environ, {'GITHUB_TOKEN': 'token'}, clear=True)
def test_main(
        mock_output_frame: Mock,
        mock_collector: Mock,
        mock_live: Mock,
        mock_spinner: Mock,
        params: list[str],
        expected_collect_params: list,
        collect_response: pd.DataFrame,
        expected_output_type: str,
    ) -> None:

    mock_collector.return_value.collect.return_value = collect_response
    runner = CliRunner()
    result = runner.invoke(main, params)

    assert mock_live.called
    assert mock_spinner.called

    assert mock_collector.call_args_list == [call(token=ANY, url='https://api.github.com', spinner=mock_spinner.return_value)]
    assert mock_collector.return_value.collect.call_args_list == expected_collect_params

    if not collect_response.empty:
        assert mock_output_frame.call_args_list == [call(collect_response, expected_output_type, spinner=mock_spinner.return_value, output_name=None)]

    assert result.exit_code == 0
