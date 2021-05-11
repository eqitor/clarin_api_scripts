from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from typing import Any
from app import schemas,crud
from app.clarinAPI.processing import CorpusProcessing
from aiofile import async_open
from random import randint
import logging
import json
import os

router = APIRouter()


@router.post("/", response_model=schemas.CorpusOut)
async def create_corpus(*,
                        zipfile: UploadFile = File(default=None),
                        metadata: UploadFile = File(default=None),
                        corpus_name: str = Form(default="Mój Korpus"),
                        background_tasks: BackgroundTasks
                        ) -> schemas.CorpusOut:
    json_data = await metadata.read()
    metadata_dict = json.loads(json_data)

    corpus_in = schemas.CorpusCreate(name=corpus_name,
                                     files=metadata_dict)
    corpus = crud.corpus.create(obj_in=corpus_in)
    _id = str(corpus.id)

    os.makedirs("temp", exist_ok=True)
    async with async_open(os.path.join("temp", f"{_id}.zip"), "wb") as file:
        content = await zipfile.read()
        await file.write(content)
    processing = CorpusProcessing(_id)
    background_tasks.add_task(processing.process_corpus)
    corpus_out = schemas.CorpusOut(
        id=corpus.id,
        name=corpus.name,
        status=corpus.status
    )
    return corpus_out


@router.get("/{corpus_id}", response_model=schemas.CorpusOut)
async def get_corpus(*,
                     corpus_id: str):
    corpus = crud.corpus.get(corpus_id)
    corpus_out = schemas.CorpusOut(
        id=corpus.id,
        name=corpus.name,
        status=corpus.status
    )
    return corpus_out

@router.get("/{corpus_id}/list")
async def get_corpus(*,
                     corpus_id: str):
    corpus = crud.corpus.get(corpus_id)
    return corpus.files

