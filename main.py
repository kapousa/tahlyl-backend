from dotenv import load_dotenv
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
import time

from lib.utils.Logger import logger
from routers import users_router, analysis_router, services_router, report_router, bloodtest_router

# Load .env
load_dotenv()

app = FastAPI()

app.include_router(users_router)
app.include_router(analysis_router)
app.include_router(services_router)
app.include_router(report_router)
app.include_router(bloodtest_router)

origins = ["http://localhost:3000/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenTelemetry Setup #########################################
# resource = Resource(attributes={
#     SERVICE_NAME: "tahlyl-services"
# })
#
# provider = TracerProvider(resource=resource)
# trace.set_tracer_provider(provider)
#
# otlp_exporter = OTLPSpanExporter(endpoint="http://127.0.0.1:4317") # Change to this.
# print(f"OTLP exporter: {otlp_exporter}") #print the exporter object.
#
# processor = BatchSpanProcessor(otlp_exporter) #Change to otlp_exporter
# provider.add_span_processor(processor)
#
# FastAPIInstrumentor.instrument_app(app)
# logger.info("OpenTelemetry Jaeger exporter initialized.")
#
# tracer = trace.get_tracer(__name__)
###################################################################################

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(json.dumps({
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "process_time": process_time,
    }))
    return response

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True
).instrument(app)

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