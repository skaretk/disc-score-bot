
import logging
import os
from typing import Optional

DEFAULT_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def configure_logging(level: Optional[str] = None) -> None:
    """ Configure root logging """
    if level is None:
        level = DEFAULT_LEVEL

    root = logging.getLogger()
    if root.handlers:  # already configured (e.g., by pytest or another framework)
        return

    # Use a StreamHandler to stdout for visibility in docker/CI/pytest -s
    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)

    root.setLevel(level)
    root.addHandler(handler)
