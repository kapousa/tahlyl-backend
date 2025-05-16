# Configure logging
import logging
import os

# Get the log level from an environment variable, default to INFO
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
numeric_level = getattr(logging, LOG_LEVEL, None)
if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {LOG_LEVEL}")

logger = logging.getLogger(__name__)
logger.setLevel(numeric_level)

# Console Handler (existing)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# File Handler (new)
log_file = "app.log"  # Specify the name of your log file
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(numeric_level)
file_formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Optional: Rotating File Handler for managing log file size
# from logging.handlers import RotatingFileHandler
# log_file = "app.log"
# maxBytes = 10 * 1024 * 1024  # 10 MB
# backupCount = 5
# rotating_file_handler = RotatingFileHandler(log_file, maxBytes=maxBytes, backupCount=backupCount, encoding='utf-8')
# rotating_file_handler.setLevel(numeric_level)
# rotating_file_formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
# rotating_file_handler.setFormatter(rotating_file_formatter)
# logger.addHandler(rotating_file_handler)




# # com/utils/Logger.py
# import logging
# import os
# import loki
#
# try:
#     from loki.handlers import LokiHandler
#     loki_handler_imported = True
# except ImportError:
#     try:
#         from loki import LokiHandler  # Try direct import
#         loki_handler_imported = True
#     except ImportError:
#         loki_handler_imported = False
#         print("Error: Could not import LokiHandler from the 'loki' library. Ensure it's installed correctly.")
#
#
# LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# numeric_level = getattr(logging, LOG_LEVEL, None)
# if not isinstance(numeric_level, int):
#     raise ValueError(f"Invalid log level: {LOG_LEVEL}")
#
# logger = logging.getLogger(__name__)
# logger.setLevel(numeric_level)
#
# # Console Handler (existing)
# stream_handler = logging.StreamHandler()
# formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}')
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)
#
# # Grafana Cloud Loki Handler
# LOKI_URL = "YOUR_LOKI_PUSH_API_URL"  # Replace with your Loki Push API URL
# LOKI_AUTH = ("gadallahhatem", "glsa_3roLUc31jKGFsvTFKQexG6N2zL6m99y1_69a062a9")  # Replace with your credentials
#
# if loki_handler_imported and LOKI_URL and LOKI_AUTH[0] and LOKI_AUTH[1]:
#     loki_handler = LokiHandler(
#         url=LOKI_URL,
#         auth=LOKI_AUTH,
#         tags={"application": "tahlyl-backend", "environment": os.environ.get("ENVIRONMENT", "development")},
#         version="1",
#     )
#     logger.addHandler(loki_handler)
#     print("Grafana Cloud Loki logging initialized.")
# else:
#     print("Grafana Cloud Loki URL or authentication not configured, or LokiHandler import failed.")
#
#
# # Optional: File Handler (keep if you still want local file logging)
# LOG_FILE = "app.log"
# file_handler = logging.FileHandler(LOG_FILE)
# file_handler.setLevel(numeric_level)
# file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
# file_handler.setFormatter(file_formatter)
# logger.addHandler(file_handler)