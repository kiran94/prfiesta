import os
from datetime import datetime
from typing import List
from unittest.mock import ANY, Mock, call, patch

import pandas as pd
import pytest
from click.testing import CliRunner

from prfiesta.__main__ import main

FAILURE_CODE = 2


@pytest.mark.parametrize(
    "arguments",
    [
        pytest.param(["--users", "user", "--use-involves", "--use-reviewed-by", "--use-review-requested"]),
        pytest.param(["--users", "user", "--use-involves", "--use-reviewed-by"]),
        pytest.param(["--users", "user", "--use-reviewed-by", "--use-review-requested"]),
        pytest.param(["--users", "user", "--use-involves", "--use-review-requested"]),
    ],
)
def test_main_author_filters_mutually_exclusive(arguments: List[str]) -> None:
    runner = CliRunner()
    result = runner.invoke(main, arguments)

    assert "the following parameters are mutually exclusive" in result.output
    assert result.exit_code == FAILURE_CODE


@pytest.mark.parametrize(
    ("params", "expected_collect_params", "collect_response", "expected_output_type", "expected_output"),
    [
        pytest.param(
            ["--users", "test_user"],
            [call("test_user", after=None, before=None, use_updated=False, use_involves=False, use_reviewed_by=False, use_review_requested=False)],
            pd.DataFrame(),
            "csv",
            None,
            id="user_provided",
        ),
        pytest.param(
            ["--users", "test_user", "--after", "2020-01-01"],
            [
                call(
                    "test_user",
                    after=datetime(2020, 1, 1),
                    before=None,
                    use_updated=False,
                    use_involves=False,
                    use_reviewed_by=False,
                    use_review_requested=False,
                ),
            ],
            pd.DataFrame(),
            "csv",
            None,
            id="with_after",
        ),
        pytest.param(
            ["--users", "test_user", "--before", "2020-01-01"],
            [
                call(
                    "test_user",
                    before=datetime(2020, 1, 1),
                    after=None,
                    use_updated=False,
                    use_involves=False,
                    use_reviewed_by=False,
                    use_review_requested=False,
                ),
            ],
            pd.DataFrame(),
            "csv",
            None,
            id="with_before",
        ),
        pytest.param(
            ["--users", "test_user", "--before", "2020-01-01", "--after", "2009-01-01"],
            [
                call(
                    "test_user",
                    before=datetime(2020, 1, 1),
                    after=datetime(2009, 1, 1),
                    use_updated=False,
                    use_involves=False,
                    use_reviewed_by=False,
                    use_review_requested=False,
                ),
            ],
            pd.DataFrame(),
            "csv",
            None,
            id="with_before_and_after",
        ),
        pytest.param(
            ["--users", "test_user"],
            [call("test_user", after=None, before=None, use_updated=False, use_involves=False, use_reviewed_by=False, use_review_requested=False)],
            pd.DataFrame(
                data=[(1, 2, 3)],
                columns=["col1", "col2", "col3"],
            ),
            "csv",
            None,
            id="with_collected_responses",
        ),
        pytest.param(
            ["--users", "test_user", "--output-type", "parquet"],
            [call("test_user", after=None, before=None, use_updated=False, use_involves=False, use_reviewed_by=False, use_review_requested=False)],
            pd.DataFrame(
                data=[(1, 2, 3)],
                columns=["col1", "col2", "col3"],
            ),
            "parquet",
            None,
            id="with_parquet",
        ),
        pytest.param(
            ["--users", "test_user", "--before", "2020-01-01", "--use-updated"],
            [
                call(
                    "test_user",
                    before=datetime(2020, 1, 1),
                    after=None,
                    use_updated=True,
                    use_involves=False,
                    use_reviewed_by=False,
                    use_review_requested=False,
                ),
            ],
            pd.DataFrame(),
            "csv",
            None,
            id="with_use_updated",
        ),
        pytest.param(
            ["--users", "test_user", "--before", "2020-01-01", "--use-involves"],
            [
                call(
                    "test_user",
                    before=datetime(2020, 1, 1),
                    after=None,
                    use_updated=False,
                    use_involves=True,
                    use_reviewed_by=False,
                    use_review_requested=False,
                ),
            ],
            pd.DataFrame(),
            "csv",
            None,
            id="with_use_involves",
        ),
        pytest.param(
            ["--users", "test_user", "--use-reviewed-by"],
            [call("test_user", after=None, before=None, use_updated=False, use_involves=False, use_reviewed_by=True, use_review_requested=False)],
            pd.DataFrame(),
            "csv",
            None,
            id="user_reviewed_by",
        ),
        pytest.param(
            ["--users", "test_user", "--use-review-requested"],
            [call("test_user", after=None, before=None, use_updated=False, use_involves=False, use_reviewed_by=False, use_review_requested=True)],
            pd.DataFrame(),
            "csv",
            None,
            id="user_review_requested",
        ),
        pytest.param(
            ["--users", "test_user", "--output-type", "duckdb", "--output", "my.duckdb"],
            [call("test_user", after=None, before=None, use_updated=False, use_involves=False, use_reviewed_by=False, use_review_requested=False)],
            pd.DataFrame(data={"a": [1, 2, 3]}),
            "duckdb",
            "my.duckdb",
            id="with_duckdb",
        ),
    ],
)
@patch("prfiesta.__main__.Spinner")
@patch("prfiesta.__main__.Live")
@patch("prfiesta.__main__.GitHubCollector")
@patch("prfiesta.__main__.output_frame")
@patch.dict(os.environ, {"GITHUB_TOKEN": "token"}, clear=True)
def test_main(
    mock_output_frame: Mock,
    mock_collector: Mock,
    mock_live: Mock,
    mock_spinner: Mock,
    params: List[str],
    expected_collect_params: List,
    collect_response: pd.DataFrame,
    expected_output_type: str,
    expected_output: str,
) -> None:
    mock_collector.return_value.collect.return_value = collect_response
    runner = CliRunner()
    result = runner.invoke(main, params)

    assert mock_live.called
    assert mock_spinner.called

    assert mock_collector.call_args_list == [call(token=ANY, url="https://api.github.com", spinner=mock_spinner.return_value, drop_columns=[])]
    assert mock_collector.return_value.collect.call_args_list == expected_collect_params

    if not collect_response.empty:
        assert mock_output_frame.call_args_list == [
            call(collect_response, expected_output_type, spinner=mock_spinner.return_value, output_name=expected_output),
        ]

    assert result.exit_code == 0
