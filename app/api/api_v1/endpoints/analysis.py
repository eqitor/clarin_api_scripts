from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from app import schemas, crud
from app.clarinAPI.analysis import TagerAnalysis, NerAnalysis, Analysis
import logging
from mongoengine.base.datastructures import BaseList, BaseDict
from typing import Optional

router = APIRouter()


@router.post("/", response_model=schemas.AnalysisOut)
async def create_analysis(*,
                          corpus_id: str,
                          filter_boundaries: Optional[dict] = None,
                          options: Optional[dict] = None,
                          background_tasks: BackgroundTasks):
    analysis_in = schemas.AnalysisCreate(
        boundaries=filter_boundaries,
        corpus_id=corpus_id,
        options=options
    )
    analysis_obj = crud.analysis.create(analysis_in)
    analysis = Analysis(corpus_id, boundaries=filter_boundaries, analysis_id=str(analysis_obj.id))

    background_tasks.add_task(analysis.start_analysis)

    analysis_out = schemas.AnalysisOut(
        id=analysis_obj.id,
        boundaries=convert_basedict_to_dict(analysis_obj.boundaries),
        corpus_id=analysis_obj.corpus_id,
        options=analysis_obj.options,
        files=analysis_obj.files,
        files_count=analysis_obj.files_count,
        result=convert_basedict_to_dict(analysis_obj.result)
    )
    # TODO zmienic ListBase na list
    return analysis_out


@router.get("/{analysis_id}")
async def get_analysis(*,
                       analysis_id: str):
    analysis_obj = crud.analysis.get(analysis_id)
    analysis_out = schemas.AnalysisOut(
        id=analysis_obj.id,
        status=analysis_obj.status,
        boundaries=convert_basedict_to_dict(analysis_obj.boundaries),
        corpus_id=analysis_obj.corpus_id,
        options=convert_basedict_to_dict(analysis_obj.options),
        files=convert_basedict_to_dict(analysis_obj.files),
        files_count=analysis_obj.files_count,
        result=convert_basedict_to_dict(analysis_obj.result)
    )
    return analysis_out


@router.get("/{analysis_id}/ner")
async def get_ner_analysis(*,
                           analysis_id: str,
                           limit: int = None):
    na = NerAnalysis(analysis_id)
    return na.get_analysis(limit)


@router.get("/{analysis_id}/tager")
async def get_tager_analysis(*,
                             analysis_id: str,
                             limit: int = None):
    ta = TagerAnalysis(analysis_id)
    return ta.get_analysis(limit)


def convert_basedict_to_dict(d: BaseDict):
    if isinstance(d, BaseList):
        d = list(d)
        d = [convert_basedict_to_dict(x) for x in d]
    elif isinstance(d, BaseDict):
        d = dict(d)
        for key, value in d.items():
            d[key] = convert_basedict_to_dict(d[key])
    return d
