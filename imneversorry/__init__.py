import os
import logging
from imneversorry.config import Config

# Enable pyrogram logging
logging.basicConfig(
    level=Config.LOGLEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)
logging.getLogger("pyrogram").setLevel(Config.LOGLEVEL_PYROGRAM)

logger = logging.getLogger('imneversorry')
