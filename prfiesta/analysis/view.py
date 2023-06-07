from datetime import datetime, timezone

import pandas as pd
from IPython.display import HTML, DisplayObject
from natural.date import duration


def _enrich_pr_link(data: pd.DataFrame) -> pd.DataFrame:
    def make_link(row: pd.Series) -> str:
        return f'<a href="{row["html_url"]}">{row["title"]}</a>'

    data['title'] = data.apply(make_link, axis=1)
    return data.drop(columns='html_url')


def view_pull_requests(data: pd.DataFrame, **kwargs) -> DisplayObject:

    as_frame: bool = kwargs.get('as_frame', False)
    relative_dates: bool = kwargs.get('relative_dates', True)
    head: int = kwargs.get('head')

    temp = data[['number', 'title', 'repository_name', 'updated_at', 'html_url']].copy()
    temp = _enrich_pr_link(temp)

    if relative_dates:
        temp['updated_at'] = pd.to_datetime(temp['updated_at'])
        temp['updated_at'] = temp['updated_at'].apply(duration, now=datetime.now(timezone.utc))

    if head:
        temp = temp.head(head)

    if as_frame:
        return temp

    return HTML(temp.to_html(escape=False, index=False))
