from fastapi import APIRouter

from app.api.api_v1.endpoints import corpus

api_router = APIRouter()
api_router.include_router(corpus.router, prefix="/corpus", tags=["corpus"])
