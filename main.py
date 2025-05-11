from dotenv import load_dotenv
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import time

from lib.utils.Logger import logger
from lib.utils.Decorators import log_activity
from routers import users_router, analysis_router, services_router, report_router, bloodtest_router

# Load .env
load_dotenv()

app = FastAPI()

app.include_router(users_router)
app.include_router(analysis_router)
app.include_router(services_router)
app.include_router(report_router)
app.include_router(bloodtest_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Assume you have some way to identify the user, e.g., from a token or session
async def get_user_id_from_request(request: Request) -> str | None:
    """
    Example function to extract user ID from the request.
    This will depend on your authentication mechanism.
    """
    # Example: Try to get user ID from a header
    user_id = request.headers.get("X-User-Id")
    if user_id:
        return user_id

    # Example: Try to get user ID from a query parameter (less common for auth)
    # user_id = request.query_params.get("user_id")
    # if user_id:
    #     return user_id

    # Example: If you have authentication middleware that stores user info in state
    # if hasattr(request.state, "user") and request.state.user:
    #     return request.state.user.get("id")

    return None

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    user_id = await get_user_id_from_request(request)
    response = await call_next(request)
    process_time = time.time() - start_time
    log_data = {
        "url": str(request.url),  # Include the full URL
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "process_time": process_time,
    }
    if user_id:
        log_data["user_id"] = user_id
    logger.info(json.dumps(log_data))
    return response

@app.on_event("startup")
async def startup():
    pass

@app.get("/")
def read_root():
    # with tracer.start_as_current_span("base_analysis_route"):
    #     return {"Hello": "World"}
    return {"Hello": "World"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Get PORT from env, default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)