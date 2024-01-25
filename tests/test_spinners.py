from unittest.mock import Mock, call

import pytest

from prfiesta import SPINNER_STYLE
from prfiesta.spinner import update_spinner


@pytest.mark.parametrize(
    ("message", "spinner", "logger"),
    [
        pytest.param("my_message", Mock(), Mock(), id="all_parameters_supplied"),
        pytest.param("my_message", None, Mock(), id="spinner_none"),
    ],
)
def test_update_spinner(message: str, spinner: Mock, logger: Mock) -> None:
    update_spinner(message, spinner, logger)

    assert logger.debug.call_args_list == [call(message)]

    if spinner:
        assert spinner.update.call_args_list == [call(text=message, style=SPINNER_STYLE)]
