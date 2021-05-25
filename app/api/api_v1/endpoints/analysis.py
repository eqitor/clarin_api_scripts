from fastapi import APIRouter, UploadFile, File, HTTPException, Form, BackgroundTasks
from app import schemas, crud
from app.clarinAPI.analysis import TagerAnalysis, NerAnalysis, Analysis, NerAnalysis_2, TagerAnalysis_2
import logging
from mongoengine.base.datastructures import BaseList,BaseDict
router = APIRouter()



@router.post("/", response_model=schemas.AnalysisOut)
async def create_analysis(*,
                          corpus_id: str,
                          filter_boundaries: dict,
                          options: dict):
    analysis_in = schemas.AnalysisCreate(
        boundaries=filter_boundaries,
        corpus_id=corpus_id,
        options=options
    )
    analysis_obj = crud.analysis.create(analysis_in)
    analysis = Analysis(corpus_id, boundaries=filter_boundaries, analysis_id=analysis_obj.id)
    analysis.start_analysis(options)

    analysis_out = schemas.AnalysisOut(
        id=analysis_obj.id,
        boundaries=convert_basedict_to_dict(analysis_obj.boundaries),
        corpus_id=analysis_obj.corpus_id,
        options=analysis_obj.options,
        files=analysis_obj.files
    )
    #TODO zmienic ListBase na list
    return analysis_out

def convert_basedict_to_dict(d: BaseDict):
    d = dict(d)
    for key, value in d.items():
        if type(value) is BaseList:
            d[key] = list(value)
        elif type(value) is BaseDict or type(value) is dict:
            d[key] = convert_basedict_to_dict(d[key])
    return d


@router.post("/tager")
async def get_tager_analysis(*,
                     corpus_id: str,
                     ctags: list,
                     limit: int = None):
    ta = TagerAnalysis(corpus_id)
    return ta.get_analysis(ctags, limit)

@router.get("/{analysis_id}/ner")
async def get_ner_analysis2(*,
                     analysis_id: str,
                     limit: int = None):
    na = NerAnalysis_2(analysis_id)
    return na.get_analysis(limit)

@router.post("/{analysis_id}/tager")
async def get_tager_analysis2(*,
                     analysis_id: str,
                     limit: int = None):
    ta = TagerAnalysis_2(analysis_id)
    return ta.get_analysis(limit)



@router.post("/ner")
async def get_ner_analysis(*,
                     corpus_id: str,
                     limit: int = None):
    na = NerAnalysis(corpus_id)
    return na.get_analysis(limit)
