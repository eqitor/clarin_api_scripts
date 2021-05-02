from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from app import schemas,crud
from app.clarinAPI.processing import CorpusProcessing
from aiofile import async_open
from app.clarinAPI.analysis import TagerAnalysis

router = APIRouter()




@router.get("/tager")
async def get_tager_analysis(*,
                     corpus_id: str):
    ta = TagerAnalysis(corpus_id)
    return ta.get_analysis()


