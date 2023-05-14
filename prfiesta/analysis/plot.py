import calendar
import logging
from typing import Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes

logger = logging.getLogger(__name__)

_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def plot_state_distribution(data: pd.DataFrame, **kwargs) -> Union[plt.Figure, plt.Axes, pd.DataFrame]:

    ax: Optional[Axes] = kwargs.get('ax')
    palette: Optional[str] = kwargs.get('palette')
    title: Optional[str] = kwargs.get('title', 'State Distribution')
    hue: Optional[str] = kwargs.get('hue', 'repository_name')

    if ax:
        ax.set_title(title)

    return sns.histplot(data, x='state', hue=hue, ax=ax, palette=palette)

def plot_overall_timeline(data: pd.DataFrame, **kwargs) -> Union[plt.Figure, plt.Axes, pd.DataFrame]:

    ax: Optional[Axes] = kwargs.get('ax')
    palette: Optional[str] = kwargs.get('palette')
    title: Optional[str] = kwargs.get('title', 'Overall Contributions')
    hue: Optional[str] = kwargs.get('hue', 'month')

    temp = data.copy()

    temp['month'] = temp['created_at'].dt.month_name()
    temp['year'] = temp['created_at'].dt.year.astype(str)

    temp = temp.groupby(['month', 'year'])['id'].count()
    temp = temp.reset_index()

    # X Axis Ordering (Year)
    x_order = temp['year'].unique().tolist()
    x_order = [int(x) for x in x_order]
    x_order.sort()
    x_order = [str(x) for x in x_order]

    # Hue Ordering (Months)
    sorted_months = sorted(_months, key=lambda x: list(calendar.month_name).index(x))

    p = sns.barplot(temp, x='year', y='id', hue=hue, ax=ax, order=x_order, hue_order=sorted_months, palette=palette)

    if ax:
        ax.set_title(title)
        ax.legend(loc='upper left')

    return p

