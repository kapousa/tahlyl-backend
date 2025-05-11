# utils/Decorators.py
import asyncio
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_activity(log_level=logging.INFO, message=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            log_msg = message if message else f"Calling function: {func.__name__}"
            logger.log(log_level, log_msg)
            try:
                result = await func(*args, **kwargs)
                logger.info(f"Function {func.__name__} completed successfully.")
                return result
            except Exception as e:
                logger.error(f"Error in function {func.__name__}: {e}")
                raise
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            log_msg = message if message else f"Calling function: {func.__name__}"
            logger.log(log_level, log_msg)
            try:
                result = func(*args, **kwargs)
                logger.info(f"Function {func.__name__} completed successfully.")
                return result
            except Exception as e:
                logger.error(f"Error in function {func.__name__}: {e}")
                raise
        if asyncio.iscoroutinefunction(func):
            return wrapper
        else:
            return sync_wrapper
    return decorator