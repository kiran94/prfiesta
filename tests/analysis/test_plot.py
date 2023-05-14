from typing import Dict
from unittest.mock import Mock, call, patch

import pandas as pd
import pytest

from prfiesta.analysis.plot import plot_state_distribution

_mock_state_distribution_axis = Mock()


@pytest.mark.parametrize(('options', 'expected_options'), [
    pytest.param(
        {'ax': _mock_state_distribution_axis},
        { 'x': 'state', 'hue': 'repository_name', 'ax': _mock_state_distribution_axis, 'palette': None },
        id='with_custom_axis'),
    pytest.param(
        {'hue': 'user.login'},
        { 'x': 'state', 'hue': 'user.login', 'ax': None, 'palette': None },
        id='with_custom_hue'),
    pytest.param(
        {'palette': 'tab10'},
        { 'x': 'state', 'hue': 'repository_name', 'ax': None, 'palette': 'tab10' },
        id='with_custom_hue'),
    pytest.param(
        {'ax': _mock_state_distribution_axis, 'title': 'my_title'},
        { 'x': 'state', 'hue': 'repository_name', 'ax': _mock_state_distribution_axis, 'palette': None },
        id='with_custom_title'),
])
@patch('prfiesta.analysis.plot.sns')
def test_plot_state_distribution(mock_seaborn: Mock, options: Dict, expected_options: Dict) -> None:

    data = pd.DataFrame(data={
        'state': ['opened', 'closed'],
        'repository_name': ['repo', 'repo2'],
        'user.login': ['user', 'user2'],
    })

    mock_histplot = Mock()
    mock_seaborn.histplot.return_value = mock_histplot

    result = plot_state_distribution(data, **options)

    if ('title' in options) and (options['title']):
        assert _mock_state_distribution_axis.set_title.call_args_list == [call(options['title'])]

    assert mock_histplot == result
    assert mock_seaborn.histplot.call_args_list == [call(data, **expected_options)]

    _mock_state_distribution_axis.reset_mock()
