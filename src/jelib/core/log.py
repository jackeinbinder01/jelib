import logging
from .status import Status

logger = logging.getLogger("jelib")


def setup_logging(
    level: int = logging.DEBUG,
    fmt: str | None = None,
    datefmt: str | None = None,
    filename: str | None = None
) -> None:
    if fmt is None:
        fmt = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
    if datefmt is None:
        datefmt = "%Y-%m-%d %H:%M:%S"

    if filename:
        logging.basicConfig(
            level=level,
            format=fmt,
            datefmt=datefmt,
            filename=filename,
            filemode="a"
        )
    else:
        logging.basicConfig(
            level=level,
            format=fmt,
            datefmt=datefmt
        )

    logger.setLevel(level)


def log_status(status: Status) -> None:
    logger.debug(f"STATUS = {status.name} ({status.value})")