import logging
import os
from datetime import datetime
from typing import Literal

import pandas as pd
from rich.spinner import Spinner

from prfiesta import SPINNER_STYLE

logger = logging.getLogger(__name__)

output_directory = 'output'
OUTPUT_TYPE = Literal['csv', 'parquet']


def output_frame(frame: pd.DataFrame, output_type: OUTPUT_TYPE, spinner: Spinner, output_name: str = 'export', timestamp: datetime = None) -> None:

    if not timestamp:
        timestamp = datetime.now()

    os.makedirs(output_directory, exist_ok=True)

    output_name = str(output_name) + '.' + timestamp.strftime('%Y-%m-%d_%H:%M:%S') + '.' + output_type
    output_name = os.path.join(output_directory, output_name)

    spinner.update(text=f'Writing export to {output_name}', style=SPINNER_STYLE)

    match output_type:
        case 'csv':
            frame.to_csv(output_name, index=False)

        case 'parquet':
            frame.to_parquet(output_name, index=False)

        case _:
            raise ValueError('unknown output_type %s', output_type)

    logger.info('Exported to %s!', output_name)
