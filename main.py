# main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Depends
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.concurrency import run_in_threadpool # Still needed for ALL sync DB ops
import uvicorn

# Import database connection functions and Base, services from config.py
from config import (
    connect_to_mongo, close_mongo_connection, get_mongo_db_sync, # For Synchronous MongoDB
    create_sqlite_tables_sync, get_sqlite_db_sync, # For Synchronous SQLite
    Base, engine # For SQLAlchemy Base and Engine in startup (synchronous)
)

# Import other components (ensure these paths are correct)
from com.services.auth.auth_backend import JWTAuthBackend
from com.utils.Logger import logger
from middleware.log_middleware import LogRequestsMiddleware
from routers import (
    users_router, analysis_router, services_router, report_router,
    bloodtest_router, smartfeatures_router, programs_router
)

# Load environment variables
load_dotenv()

# --- FastAPI Application Instance ---
app = FastAPI(
    title="Tahlyl: AI-Powered Medical Test Analysis API Platform",
    description="API for understanding and managing medical test results with AI.",
    version="0.1.0"
)


# --- Middleware Registration Order ---
app.add_middleware(LogRequestsMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"], # Consider narrowing this down for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Include Routers ---
app.include_router(users_router)
app.include_router(analysis_router)
app.include_router(services_router)
app.include_router(report_router)
app.include_router(bloodtest_router)
app.include_router(smartfeatures_router)
app.include_router(programs_router)


# --- Global Exception Handlers ---
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"Unhandled exception for request: {request.method} {request.url}",
        exc_info=True,
        extra={
            "request_id": getattr(request.state, "request_id", "N/A"),
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
    )
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected server error occurred. Please try again later.",
            "request_id": getattr(request.state, "request_id", "N/A"),
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(
        f"HTTP Exception: {exc.status_code} - {exc.detail} for request: {request.method} {request.url}",
        extra={
            "request_id": getattr(request.state, "request_id", "N/A"),
            "status_code": exc.status_code,
            "detail": exc.detail,
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "request_id": getattr(request.state, "request_id", "N/A")},
    )

@app.on_event("startup")
def startup_event():
    logger.info("FastAPI application startup event triggered.")
    create_sqlite_tables_sync() # Ensure SQLite tables are created (can be here or at global scope)
    connect_to_mongo() # Establish MongoDB connection for this worker process

@app.on_event("shutdown")
def shutdown_event():
    logger.info("FastAPI application shutdown event triggered.")
    close_mongo_connection()

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)