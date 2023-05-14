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

