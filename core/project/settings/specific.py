import logging

from .main import *  # noqa


DEBUG = False  # noqa

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

STATICFILES_DIRS = [
    BASE_DIR / "frontend/static",  # noqa
]
STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa

MEDIA_URL = "frontend/media/"
MEDIA_ROOT = "frontend/media/"
