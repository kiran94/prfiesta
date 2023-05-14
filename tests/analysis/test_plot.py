from datetime import datetime
from typing import Dict
from unittest.mock import ANY, Mock, call, patch

import pandas as pd
import pytest

from prfiesta.analysis.plot import _months, plot_author_associations, plot_overall_timeline, plot_state_distribution

_mock_state_distribution_axis = Mock()
_mock_overall_timeline_axis = Mock()
_mock_author_association_axis = Mock()


@pytest.mark.parametrize(('options', 'expected_options'), [
    pytest.param(
        {},
        { 'x': 'state', 'hue': 'repository_name', 'ax': None, 'palette': None },
        id='default'),
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


@pytest.mark.parametrize(('options', 'expected_options'), [
   pytest.param(
        {},
        {'x':'year', 'y':'id', 'hue':'month', 'ax': None, 'order':['2021', '2022'], 'hue_order':_months, 'palette':None},
        id='default',
    ),
   pytest.param(
        {'ax': _mock_overall_timeline_axis },
        {'x':'year', 'y':'id', 'hue':'month', 'ax': _mock_overall_timeline_axis, 'order':['2021', '2022'], 'hue_order':_months, 'palette':None},
        id='with_custom_axis',
    ),
   pytest.param(
        {'palette': 'tab10'},
        {'x':'year', 'y':'id', 'hue':'month', 'ax': None, 'order':['2021', '2022'], 'hue_order':_months, 'palette':'tab10'},
        id='with_custom_pallete',
    ),
   pytest.param(
        { 'ax': _mock_overall_timeline_axis, 'title': 'my_title'},
        {'x':'year', 'y':'id', 'hue':'month', 'ax': _mock_overall_timeline_axis, 'order':['2021', '2022'], 'hue_order':_months, 'palette':None},
        id='with_custom_title',
    ),
   pytest.param(
        {'hue': 'custom_field'},
        {'x':'year', 'y':'id', 'hue':'custom_field', 'ax': None, 'order':['2021', '2022'], 'hue_order':_months, 'palette':None},
        id='with_custom_hue',
    ),
])
@patch('prfiesta.analysis.plot.sns')
def test_plot_overall_timeline(mock_seaborn: Mock, options: Dict, expected_options: Dict) -> None:

    mock_barplot = Mock()
    mock_seaborn.barplot.return_value = mock_barplot

    data = pd.DataFrame(data={
        'created_at': [datetime(2021, 1, 1), datetime(2021, 2, 1), datetime(2022, 4, 14)],
        'id': ['id1', 'id2', 'id3'],
    })

    result = plot_overall_timeline(data, **options)

    assert mock_barplot == result
    assert mock_seaborn.barplot.call_args_list == [call(ANY, **expected_options)]

    if ('title' in options) and (options['title']):
        assert _mock_overall_timeline_axis.set_title.call_args_list == [call(options['title'])]

    _mock_overall_timeline_axis.reset_mock()


@pytest.mark.parametrize(('options', 'expected_options'), [
   pytest.param(
        {},
        {'ax': None, 'title': 'Author Associations', 'legend': True, 'colormap': None},
        id='default',
    ),
   pytest.param(
        {'ax': _mock_author_association_axis},
        {'ax': _mock_author_association_axis, 'title': 'Author Associations', 'legend': True, 'colormap': None},
        id='with_custom_axis',
    ),
   pytest.param(
        {'title': 'my_custom_title'},
        {'ax': None, 'title': 'my_custom_title', 'legend': True, 'colormap': None},
        id='with_custom_title',
    ),
   pytest.param(
        {'palette': 'my_colors'},
        {'ax': None, 'title': 'Author Associations', 'legend': True, 'colormap': 'my_colors'},
        id='with_custom_pallete',
    ),
])
def test_plot_author_associations(options: Dict, expected_options: Dict) -> None:

    agg_mock = Mock()

    data = Mock()
    data.groupby = Mock(return_value = {'id': Mock()})
    data.groupby.return_value['id'] = agg_mock

    plot_author_associations(data, **options)

    assert data.groupby.called
    assert agg_mock.count.called
    assert agg_mock.count.return_value.plot.pie.call_args_list == [call(**expected_options)]
