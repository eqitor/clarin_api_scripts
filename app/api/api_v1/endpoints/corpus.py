from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from typing import Any
from app import schemas,crud
from app.clarinAPI.processing import CorpusProcessing
from aiofile import async_open
from random import randint
import logging

router = APIRouter()


@router.post("/", response_model=schemas.Corpus)
async def create_corpus(*,
                        zipfile: UploadFile = File(default=None),
                        corpus_name: str = Form(default="Korpus"),
                        background_tasks: BackgroundTasks
                        ) -> schemas.Corpus:
    corpus_in = schemas.CorpusCreate(name=corpus_name)
    corpus_out = crud.corpus.create(obj_in=corpus_in)
    _id = str(corpus_out.id)
    async with async_open(f"temp/{_id}.zip", "wb") as file:
        content = await zipfile.read()
        await file.write(content)
    processing = CorpusProcessing(_id)
    background_tasks.add_task(processing.process_corpus)
    return corpus_out


@router.get("/{corpus_id}", response_model=schemas.Corpus)
async def get_corpus(*,
                     corpus_id: str):
    return crud.corpus.get(corpus_id)


@router.post("/{corpus_id}/analysis")
async def process_corpus(*,
                         corpus_id: str):
    processing = CorpusProcessing(corpus_id)
    await processing.process_corpus()
    return {"status": "ok"}

