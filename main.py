# main.py

import os
import json
import time
import traceback
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import uvicorn

# Assuming these are your custom imports
from com.engine.auth.auth_backend import JWTAuthBackend
from com.models.APILog import APILog
from com.utils import Helper
from com.utils.Logger import logger
# Updated import path for LogRequestsMiddleware based on typical structure
from middleware.log_middleware import LogRequestsMiddleware


from routers import users_router, analysis_router, services_router, report_router, bloodtest_router, smartfeatures_router

from config import SessionLocal, Base, engine


# Create tables if not exist
Base.metadata.create_all(bind=engine)

# Load .env variables (for local development)
load_dotenv()

# --- Environment Configuration for CORS ---
# Get the environment from an environment variable, defaulting to 'development'
# For production on Render, set APP_ENV=production in Render's environment settings.
APP_ENV = os.getenv("APP_ENV", "development")

# Define your allowed origins based on the environment
if APP_ENV == "production":
    allowed_origins = [
        "https://tahlyl-frontend.netlify.app",
        # Add any other production domains if needed
    ]
else: # 'development' or any other non-production environment
    allowed_origins = [
        "http://localhost:8080",
        "http://127.0.0.1:8080", # Include both for robustness in local development
        # Add any other local development URLs if your frontend runs on different ports or IPs
    ]
# --- End Environment Configuration ---


app = FastAPI(
    title="Tahlyl: AI-Powered Medical Test Analysis API Platform",
    description="API for understanding and managing medical test results with AI.",
    version="0.1.0"
)

# --- Include Routers ---
app.include_router(users_router)
app.include_router(analysis_router)
app.include_router(services_router)
app.include_router(report_router)
app.include_router(bloodtest_router)
app.include_router(smartfeatures_router)


# --- Middleware Registration Order ---
# Middleware execute in the order they are added.
# LogRequestsMiddleware should ideally be first to log all requests.
app.add_middleware(LogRequestsMiddleware)
# AuthenticationMiddleware comes next to process auth headers.
app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
# CORSMiddleware should be placed after any middleware that might send responses
# before CORS checks, but before route handling.
app.add_middleware(
    CORSMiddleware,
    allow_origins="https://tahlyl-frontend.netlify.app", # Dynamically set based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def startup():
    pass

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)