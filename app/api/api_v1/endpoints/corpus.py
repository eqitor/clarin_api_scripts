from fastapi import APIRouter, UploadFile, File
from typing import Any
from app import schemas
from app.clarinAPI.TagerAPI import FileTask
from time import sleep
from random import randint

router = APIRouter()


@router.post("/")
async def create_corpus(*,
                        zipfile: UploadFile = File(default="None")
                        ) -> Any:
    id = randint(0,100000)
    with open(f"temp/{id}.zip", "wb") as file:
        content = await zipfile.read()
        file.write(content)
    return {"id": f"{id}"}


@router.post("/{corpus_id}/analysis")
async def process_corpus(*,
                         corpus_id: int,
                         full: bool = True):
    task = FileTask(f"temp/{corpus_id}.zip")
    i = 0
    while not task.is_ready():
        sleep(0.1)
        i += 1
        if i > 600:
            break
    else:
        file = f"temp/{corpus_id}_result.zip"
        task.download_and_save_file(out_file=file)
        return {"status": "ok"}
    return {"status": "error"}