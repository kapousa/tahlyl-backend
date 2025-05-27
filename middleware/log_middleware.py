# log_middleware.py
import time
import json
import traceback
from datetime import datetime, timedelta
from http import HTTPStatus
import logging  # Using standard Python logging

from fastapi import Request
from sqlalchemy.orm import Session

# Adjust these imports to your actual project structure
# Assuming your APILog model is in com.models.APILog
from com.models.APILog import APILog
# Assuming your logger is in com.utils.Logger
from com.utils.Logger import logger
# Assuming your SessionLocal is in config (or database.py)
from config import SessionLocal


async def log_requests_middleware(request: Request, call_next):
    """
    Middleware to log details of each API request, including authenticated user ID.
    """
    start_time = time.time()
    user_id_for_log = None

    # Check if request.user is available and authenticated by AuthenticationMiddleware
    if request.user and request.user.is_authenticated:
        # Assuming request.user.identity holds the user ID (from your AuthenticatedUser class)
        user_id_for_log = request.user.identity
    else:
        # For unauthenticated requests or those where auth failed, log as 'None' or 'anonymous'
        user_id_for_log = "anonymous"  # Or simply None, depending on your logging preference

    log_data = {
        "method": request.method,
        "path": request.url.path,
        "timestamp": datetime.utcnow(),
        "user_id": user_id_for_log
    }

    response = None  # Initialize response outside try block
    db: Session = None  # Initialize db outside try block to ensure it's closed

    try:
        # Proceed to the next middleware or route handler
        response = await call_next(request)

        log_data["status_code"] = response.status_code
        log_data["status_description"] = HTTPStatus(response.status_code).phrase

    except Exception as e:
        # This catches any unhandled exceptions from downstream middleware or route handlers
        log_data["status_code"] = 500
        log_data["status_description"] = HTTPStatus(500).phrase
        log_data["error_message"] = str(e)
        log_data["traceback"] = traceback.format_exc()
        raise  # Re-raise the exception after logging it so FastAPI can handle it further
    finally:
        log_data["duration"] = str(timedelta(seconds=time.time() - start_time))

        # Acquire a new DB session specifically for logging, just in case the request's session was closed/rolled back
        db = SessionLocal()
        try:
            db.add(APILog(**log_data))
            db.commit()
        except Exception as db_exc:
            logger.error(f"Failed to save log to DB: {db_exc}", exc_info=True)
            db.rollback()  # Ensure rollback on DB save error
        finally:
            if db:  # Ensure db session is closed if it was opened
                db.close()

        # Log the full request data to your existing logger
        logger.info(json.dumps(log_data, default=str))

    return response