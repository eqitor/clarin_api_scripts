from bson import ObjectId
from pydantic import BaseModel
from typing import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class AnalysisBase(BaseModel):
    status: str = "PROCESSING"
    boundaries: dict
    corpus_id: str
    options: dict


class AnalysisCreate(AnalysisBase):
    pass


class AnalysisOut(AnalysisBase):
    id: PyObjectId

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }


class Analysis(BaseModel):
    id: PyObjectId
    files: Optional[list]
    status: str
    boundaries: dict
    options: dict
    corpus_id: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }

