# Configure logging
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')
handler.setFormatter(formatter)
logger.addHandler(handler)