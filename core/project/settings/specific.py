import logging

from .main import *  # noqa


DEBUG = True  # noqa

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
