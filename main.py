import sentry_sdk
import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

import settings
from api.handlers import user_router
from api.login_handler import login_router
from api.service import service_router

sentry_sdk.init(
    dsn=settings.SENTRY_URL,
    traces_sample_rate=1.0,
)

app = FastAPI(
    title="Educational platform",
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(service_router, tags=["service"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    uvicorn.run("main:app", host="localhost", port=settings.APP_PORT, reload=True)
