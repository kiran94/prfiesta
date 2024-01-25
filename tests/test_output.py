from datetime import datetime
from unittest.mock import ANY, Mock, call, patch

import pytest

from prfiesta.output import output_frame


@pytest.mark.parametrize(
    ("output_type", "timestamp"),
    [
        pytest.param("csv", datetime(2021, 1, 1), id="csv_with_timestamp"),
        pytest.param("parquet", datetime(2021, 1, 1), id="parquet_with_timestamp"),
        pytest.param("csv", None, id="csv_without_timestamp"),
        pytest.param("parquet", None, id="parquet_without_timestamp"),
    ],
)
def test_output_frame(output_type: str, timestamp: datetime) -> None:
    mock_frame: Mock = Mock()
    mock_spinner: Mock = Mock()

    output_frame(mock_frame, output_type, mock_spinner, timestamp=timestamp)

    assert mock_spinner.update.called

    if timestamp and output_type == "csv":
        assert [call("export.20210101000000.csv", index=False)] == mock_frame.to_csv.call_args_list

    elif timestamp and output_type == "parquet":
        assert [call("export.20210101000000.parquet", index=False)] == mock_frame.to_parquet.call_args_list

    elif not timestamp and output_type == "csv":
        assert [call(ANY, index=False)] == mock_frame.to_csv.call_args_list

    elif not timestamp and output_type == "parquet":
        assert [call(ANY, index=False)] == mock_frame.to_parquet.call_args_list


def test_output_frame_unknown_type() -> None:
    mock_frame: Mock = Mock()
    mock_spinner: Mock = Mock()

    with pytest.raises(ValueError, match="unknown output_type"):
        output_frame(mock_frame, "unknown_type", mock_spinner, timestamp=datetime(2021, 1, 1))


@patch("prfiesta.output.duckdb")
def test_output_duckdb(mock_duckdb: Mock) -> None:
    mock_frame: Mock = Mock()
    mock_spinner: Mock = Mock()

    mock_duckdb_connection = Mock()
    mock_duckdb.connect.return_value = mock_duckdb_connection

    timestamp = datetime(2021, 1, 1)
    output_frame(mock_frame, "duckdb", mock_spinner, timestamp=timestamp)

    assert mock_duckdb.connect.called
    assert mock_duckdb_connection.execute.call_args_list == [call("CREATE TABLE prfiesta_20210101_000000 AS SELECT * FROM frame")]
    assert mock_duckdb_connection.close.called


@pytest.mark.parametrize(
    "filename",
    [
        "illegal:filename.csv",
        "<illegalfilename.csv",
        "illegalfilename.csv>",
        'illegal"filename.csv',
        "/illegalfilename.csv",
        "illegalfilename.\\csv",
        "illegalfilename|.csv",
        "*illegalfilename.csv",
        "illegalfilename.csv?",
    ],
)
@patch("os.name", "nt")
def test_output_illegal_filename_windows(filename: str) -> None:
    with pytest.raises(ValueError, match="is an invalid filename on windows"):
        output_frame(frame=Mock(), output_type="csv", spinner=Mock(), output_name=filename, timestamp=datetime(2021, 1, 1))
