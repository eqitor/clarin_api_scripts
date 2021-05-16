from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from app import schemas,crud
from app.clarinAPI.processing import CorpusProcessing
from aiofile import async_open
from app.clarinAPI.analysis import TagerAnalysis

router = APIRouter()


# @router.post("/")
# async def create_anaylysis(corpus_id:str, filters:dict):
#     analysis_id = 1
#     return analysis_id

@router.post("/tager")
async def get_tager_analysis(*,
                     corpus_id: str,
                     ctags: list,
                     limit: int = None):
    ta = TagerAnalysis(corpus_id)
    return ta.get_analysis(ctags, limit)
