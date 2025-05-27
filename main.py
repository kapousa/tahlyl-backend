from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import time
import traceback
from datetime import datetime, timedelta
from com.models.APILog import APILog
from com.utils import Helper
from com.utils.Logger import logger  # Your existing logger
from routers import users_router, analysis_router, services_router, report_router, bloodtest_router, smartfeatures_router

from config import SessionLocal, Base, engine  # Your DB config


# Create tables if not exist
Base.metadata.create_all(bind=engine)

# Load .env
load_dotenv()

app = FastAPI(
    title="Tahlyl: AI-Powered Medical Test Analysis API Platform",
    description="API for understanding and managing medical test results with AI.",
    version="0.1.0"
)

app.include_router(users_router)
app.include_router(analysis_router)
app.include_router(services_router)
app.include_router(report_router)
app.include_router(bloodtest_router)
app.include_router(smartfeatures_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_user_id_from_request(request: Request) -> str | None:
    user_id = "e3d593f4-0463-4cca-b83c-b4c7c641178c" #request.headers.get("X-User-Id")
    return user_id

from http import HTTPStatus  # <-- Import this

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    user_id = await get_user_id_from_request(request)
    db = SessionLocal()
    log_data = {
        "method": request.method,
        "path": request.url.path,
        "timestamp": datetime.utcnow(),
        "user_id": user_id
    }
    try:
        response = await call_next(request)
        log_data["status_code"] = response.status_code
        log_data["status_description"] = HTTPStatus(response.status_code).phrase
    except Exception as e:
        log_data["status_code"] = 500
        log_data["status_description"] = HTTPStatus(500).phrase
        log_data["error_message"] = str(e)
        log_data["traceback"] = traceback.format_exc()
        raise
    finally:
        log_data["id"] = Helper.generate_id()
        log_data["duration"] = str(timedelta(seconds=time.time() - start_time))
        try:
            db.add(APILog(**log_data))
            db.commit()
        except Exception as db_exc:
            logger.error(f"Failed to save log to DB: {db_exc}")
            db.rollback()
        finally:
            db.close()

        # Log to your existing logger as JSON string for easier parsing
        logger.info(json.dumps(log_data, default=str))

    return response


@app.on_event("startup")
async def startup():
    pass

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
