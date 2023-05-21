import importlib.metadata
import logging
import os

from rich.logging import RichHandler

__version__ = importlib.metadata.version(__name__)

LOGGING_LEVEL=os.environ.get('LOGGING_LEVEL', logging.INFO)
LOGGING_FORMAT=os.environ.get('LOGGING_FORMAT', '%(message)s')
SPINNER_STYLE=os.environ.get('SPINNER_STYLE', 'blue')

logging.basicConfig(
    level=LOGGING_LEVEL,
    format=LOGGING_FORMAT,
    handlers=[RichHandler(markup=True, show_path=False, show_time=False, show_level=True)],
)
