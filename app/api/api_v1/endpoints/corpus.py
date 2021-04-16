from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Any
from app import schemas
from app.clarinAPI.processing import CorpusProcessing
from time import sleep
from random import randint
import logging
import asyncio

router = APIRouter()



@router.post("/")
async def create_corpus(*,
                        zipfile: UploadFile = File(default="None")
                        ) -> Any:
    id = randint(0, 100000)
    with open(f"temp/{id}.zip", "wb") as file:
        content = await zipfile.read()
        file.write(content)
    return {"id": f"{id}"}


@router.post("/{corpus_id}/analysis")
async def process_corpus(*,
                         corpus_id: int,
                         full: bool = True):
    processing = CorpusProcessing(corpus_id)
    await processing.process_corpus()
    return {"status": "ok"}

