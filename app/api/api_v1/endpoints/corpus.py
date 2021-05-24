from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from typing import Any
from app import schemas,crud
from app.clarinAPI.processing import CorpusProcessing
from aiofile import async_open
from copy import deepcopy
from random import randint
from mongoengine.base.datastructures import BaseList, BaseDict
import logging
import json
import os
from app.clarinAPI.filtering import Filtering

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
    filtr = Filtering()
    filters = filtr.get_filters_schema_from_dict(metadata_dict)
    corpus_in = schemas.CorpusCreate(name=corpus_name,
                                     files=metadata_dict,
                                     filters=filters)
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
        status=corpus.status,
        filters=corpus.filters
    )

    logging.warning(filters)
    return corpus_out


@router.get("/{corpus_id}", response_model=schemas.CorpusOut)
async def get_corpus(*,
                     corpus_id: str):
    corpus = crud.corpus.get(corpus_id)
    logging.warning(type(corpus.filters))
    corpus_out = schemas.CorpusOut(
        id=corpus.id,
        name=corpus.name,
        status=corpus.status,
        filters=convert_basedict_to_dict(corpus.filters)
    )
    return corpus_out

def convert_basedict_to_dict(d: BaseDict):
    d = dict(d)
    for key, value in d.items():
        if type(value) is BaseList:
            d[key] = list(value)
        elif type(value) is BaseDict or type(value) is dict:
            d[key] = convert_base_dict_to_dict(d[key])
    return d

@router.get("/{corpus_id}/list")
async def get_corpus(*,
                     corpus_id: str):
    corpus = crud.corpus.get(corpus_id)
    return corpus.files

