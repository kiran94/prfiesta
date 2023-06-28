# Analysis

prfiesta ships with built in plots to help analyze your pull request data. These serve as a starting point in your analysis.

**It's recommended to run these within the context of a [Jupyter Notebook](https://docs.jupyter.org/en/latest/)**

## Built In Views

| View                                       | Description                                                                                                                  | Sample                                              |
| ---------------                            | ---------------                                                                                                              | -------------                                       |
| `prfiesta.analysis.view.view_pull_requests` | Produces a table of pull requests which summarizes contribution. Each pull request is linked to enable further investigation | [Link](../notebooks/views/view_pull_requests.ipynb) |

## Built In Plots

  Plot                                                        | Description                                                                                                                                                                                                                                                      | Sample                                                              |
| ---------------                                             | ---------------                                                                                                                                                                                                                                                  | ------                                                              |
| `prfiesta.analysis.plot.plot_overall_timeline`              | Produces a plot showing contributions over time catagorized by month and year                                                                                                                                                                                    | [Link](../notebooks/plots/plot_overall_contribution_timeline.ipynb) |
| `prfiesta.analysis.plot.plot_state_distribution`            | Produces a plot showing the distribution of state (open or closed PR) catagorized by repository                                                                                                                                                                  | [Link](../notebooks/plots/plot_state_distribution.ipynb)            |
| `prfiesta.analysis.plot.plot_author_associations`           | Produces a plot showing authors association to the repository contributed to                                                                                                                                                                                      | [Link](../notebooks/plots/plot_author_association.ipynb)            |
| `prfiesta.analysis.plot.plot_conventional_commit_breakdown` | Produces a plot showing [git conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) breakdown for contributions catagorized by repository name. Note that this requires the user to use conventional commit messages in their pull request titles. | [Link](../notebooks/plots/plot_conventional_commit_breakdown.ipynb) |
| `prfiesta.analysis.plot.plot_reactions`                     | Produces a plot showing distribution of [GitHub Reactions](https://docs.github.com/en/rest/reactions?apiVersion=2022-11-28)                                                                                                                                      | [Link](../notebooks/plots/plot_reactions.ipynb)                     |


All prfiesta plots have the same signature:

```python
def plot_NAME(data: pd.DataFrame, **kwargs) -> Union[plt.Figure, plt.Axes]:
    ...
```

*Where `NAME` is the placeholder for the actual plot name.*

- The plotting functions always take a `pd.DataFrame` as the first argument. This Dataframe should originate from the prfiesta collection process.
- The plotting functions always return something which can be displayed in a Jupyter Notebook
- The plotting functions always take `**kwargs` which can be used to further customize the output
    - The exact specifics of this is up to the plotting function however in general the following common *optional* options should exist:

| Option           | Type                             | Description                                                                                                                                                                                    |
| ---------------- | ---------------                  | ---------------                                                                                                                                                                                |
| `ax`             | `Optional[matplotlib.axes.Axes]` | The `matplotlib` axis to plot into. This allows users to add the plot into a `plt.subplots`. If omitted, the plot will just plot into the default location                                     |
| `palette`        | `Optional[str]`                  | A color palette to apply to the plot (e.g a [seaborn color palette](https://seaborn.pydata.org/tutorial/color_palettes.html))                                                                  |
| `title`          | `Optional[str]`                  | The title of the plot                                                                                                                                                                          |
| `hue`            | `Optional[str]`                  | Used to distinguise different catagories. This is relevant to [seaborn backed plots](https://seaborn.pydata.org/tutorial/color_palettes.html?highlight=hue#vary-hue-to-distinguish-categories) |


## Building a Custom Plot

You can build your own plot by creating a function that follows this signature:

```python
from typing import Union
import pandas as pd
import matplotlib.pyplot as plt

def plot_my_cool_plot(data: pd.DataFrame, **kwargs) -> Union[plt.Figure, plt.Axes, pd.DataFrame]:
    pass
```

All prfiesta should accept the same `kwargs` mentioned in the above table however implementation of these `kwargs` per plot is on a best effort basis.

**If you build a plot which you think will be useful for others then feel free to contribute it to this project 🚀**
