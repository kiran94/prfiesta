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

def plot_author_associations(data: pd.DataFrame, **kwargs) -> Union[plt.Figure, plt.Axes, pd.DataFrame]:

    ax: Optional[Axes] = kwargs.get('ax')
    palette: Optional[str] = kwargs.get('palette')
    title: Optional[str] = kwargs.get('title', 'Author Associations')

    temp = data.groupby('author_association')['id'].count()
    temp.name = 'count'

    return temp.plot.pie(ax=ax, title=title, legend=True, colormap=palette)

def plot_conventional_commit_breakdown(data: pd.DataFrame, **kwargs) -> Union[plt.Figure, plt.Axes, pd.DataFrame]:

    ax: Optional[Axes] = kwargs.get('ax')
    palette: Optional[str] = kwargs.get('palette')
    title: Optional[str] = kwargs.get('title', 'Conventional Commit Breakdown')
    hue: Optional[str] = kwargs.get('hue', 'type')

    conventional_commit_frame = data['title'] \
        .str \
        .extract(r'^(?P<type>feat|fix|docs|style|refactor|test|chore|build|ci|perf)(\((?P<scope>[A-Za-z-]+)\))?: (?P<subject>[^\n]+)$').copy()

    conventional_commit_frame = conventional_commit_frame.drop(columns=[1, 'subject'])
    conventional_commit_frame = pd.concat([conventional_commit_frame, data['repository_name']], axis=1)
    conventional_commit_frame = conventional_commit_frame.dropna(subset=['type'])

    if conventional_commit_frame.empty:
        logger.warning('passed data did not seem to have any conventional commits')
        return None

    type_count = conventional_commit_frame.groupby(['type', 'repository_name']).count().reset_index()
    type_count = type_count[type_count['scope'] != 0]
    type_count = type_count.sort_values(by='scope', ascending=False)
    type_count = type_count.rename(columns={'scope': 'count'})

    p = sns.barplot(type_count, y='repository_name', x='count', hue=hue, ax=ax, palette=palette)

    if ax:
        ax.set_title(title)
        ax.legend(loc='upper right')

    return p

def plot_reactions(data: pd.DataFrame, **kwargs) -> Union[plt.Figure, plt.Axes, pd.DataFrame]:

    ax: Optional[Axes] = kwargs.get('ax')
    palette: Optional[str] = kwargs.get('palette')
    title: Optional[str] = kwargs.get('title', 'Reactions')
    hue: Optional[str] = kwargs.get('hue')
    threshold: Optional[int] = kwargs.get('threshold')

    reaction_columns = [x for x in data.columns.tolist() if x.startswith('reactions.') and x not in ['reactions.url']]

    reaction_df = data[reaction_columns]
    reaction_df = reaction_df[reaction_df['reactions.total_count'] > 0]
    reaction_df = reaction_df.drop(columns=['reactions.total_count'])

    if reaction_df.empty:
        logger.warning('passed data did not seem to have any reactions 🙁')
        return None

    if threshold:
        reaction_df = reaction_df[reaction_df < threshold]

    p = sns.scatterplot(reaction_df, ax=ax, palette=palette, hue=hue)

    if ax:
        ax.set_title(title)
        ax.legend(loc='upper right')

    return p
