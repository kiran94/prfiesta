from logging import Logger

from rich.spinner import Spinner

from prfiesta import SPINNER_STYLE


def update_spinner(message: str, spinner: Spinner, logger: Logger) -> None:
    logger.debug(message)
    if spinner:
        spinner.update(text=message, style=SPINNER_STYLE)
