import os
from datetime import datetime
from unittest.mock import ANY, Mock, call, patch

import pytest

from prfiesta.output import output_frame


@pytest.mark.parametrize(('output_type', 'timestamp'), [
    ('csv', datetime(2021, 1, 1)),
    ('parquet', datetime(2021, 1, 1)),
    ('csv', None),
    ('parquet', None),
])
@patch('prfiesta.output.os')
def test_output_frame(mock_os: Mock, output_type: str, timestamp: datetime) -> None:

    mock_frame: Mock = Mock()
    mock_spinner: Mock = Mock()
    mock_os.path.join = os.path.join

    output_frame(mock_frame, output_type, mock_spinner, timestamp=timestamp)

    assert [call('output', exist_ok=True)] == mock_os.makedirs.call_args_list
    assert mock_spinner.update.called

    if timestamp and output_type == 'csv':
        assert [call('output/export.2021-01-01_00:00:00.csv', index=False)] == mock_frame.to_csv.call_args_list

    elif timestamp and output_type == 'parquet':
        assert [call('output/export.2021-01-01_00:00:00.parquet', index=False)] == mock_frame.to_parquet.call_args_list

    elif not timestamp and output_type == 'csv':
        assert [call(ANY, index=False)] == mock_frame.to_csv.call_args_list

    elif not timestamp and output_type == 'parquet':
        assert [call(ANY, index=False)] == mock_frame.to_parquet.call_args_list

@patch('prfiesta.output.os')
def test_output_frame_unknown_type(mock_os: Mock) -> None:

    mock_frame: Mock = Mock()
    mock_spinner: Mock = Mock()
    mock_os.path.join = os.path.join

    with pytest.raises(ValueError, match='unknown output_type'):
        output_frame(mock_frame, 'unknown_type', mock_spinner, timestamp=datetime(2021, 1, 1))
