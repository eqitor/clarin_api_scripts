from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging
from app.api.api_v1.api import api_router
from app.core.config import settings

logging.getLogger().setLevel(logging.DEBUG)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", debug=True
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
