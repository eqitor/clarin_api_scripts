from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from app import schemas,crud
from app.clarinAPI.processing import CorpusProcessing
from aiofile import async_open

router = APIRouter()




@router.get("/", response_model=schemas.Corpus)
async def get_corpus(*,
                     corpus_id: str,
                     tager: bool):
    return crud.corpus.get(corpus_id)


@router.post("/{corpus_id}/analysis")
async def process_corpus(*,
                         corpus_id: str):
    processing = CorpusProcessing(corpus_id)
    await processing.process_corpus()
    return {"status": "ok"}

