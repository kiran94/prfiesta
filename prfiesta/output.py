import logging
import os
import re
from datetime import datetime
from typing import Literal

import duckdb
import pandas as pd
from rich.spinner import Spinner

from prfiesta.spinner import update_spinner

logger = logging.getLogger(__name__)

OUTPUT_TYPE = Literal['csv', 'parquet', 'duckdb']
WIN_ILLEGAL_FILENAME = r'[:\/\\\*\?\"\<\>\|]'

def output_frame(
        frame: pd.DataFrame,
        output_type: OUTPUT_TYPE,
        spinner: Spinner,
        output_name: str = None,
        timestamp: datetime = None) -> None:

    if not timestamp:
        timestamp = datetime.now()

    if not output_name:
        output_name = f"export.{timestamp.strftime('%Y%m%d%H%M%S')}.{output_type}"

    if os.name == 'nt' and re.search(WIN_ILLEGAL_FILENAME, output_name):
        msg = f'{output_name} is an invalid filename on windows'
        raise ValueError(msg)

    update_spinner(f'Writing export to {output_name}', spinner, logger)

    if output_type == 'csv':
        frame.to_csv(output_name, index=False)

    elif output_type == 'parquet':
        frame.to_parquet(output_name, index=False)

    elif output_type == 'duckdb':
        duckdb_table = f"prfiesta_{timestamp.strftime('%Y%m%d_%H%M%S')}"

        update_spinner(f'connecting to duckdb {output_name}', spinner, logger)
        conn = duckdb.connect(output_name)

        update_spinner(f'exporting to duckdb table {duckdb_table}', spinner, logger)
        conn.execute(f'CREATE TABLE {duckdb_table} AS SELECT * FROM frame') # noqa: duckdb_table is always constructed internally

        conn.close()
    else:
        raise ValueError('unknown output_type %s', output_type)

    logger.info('Exported to %s!', output_name)
