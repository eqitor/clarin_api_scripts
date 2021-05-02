from fastapi import APIRouter

from app.api.api_v1.endpoints import corpus,analysis


api_router = APIRouter()
api_router.include_router(corpus.router, prefix="/corpus", tags=["corpus"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
