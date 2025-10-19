import logging
from .core.log import logger, setup_logging, log_status
from .core.status import Status


def init_project(debug: bool = False, logfile: str | None = None) -> None:
    """
    Initializes logging and core configuration for projects using jelib.

    Parameters:
        debug (bool): If True, sets logging level to DEBUG, else INFO.
        logfile (str | None): If provided, logs will be written to the file.
    """
    level = logging.DEBUG if debug else logging.INFO
    setup_logging(level=level, filename=logfile)
    logger.info("Project initialized using jelib.")


__all__ = [
    "init_project",
    "setup_logging",
    "log_status",
    "logger",
    "Status",
]
