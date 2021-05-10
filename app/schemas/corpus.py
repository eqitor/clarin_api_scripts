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


class CorpusBase(BaseModel):
    name: str = "korpus"
    status: str = "PROCESSING"


class CorpusCreate(CorpusBase):
    files: dict = None


class Corpus(BaseModel):
    id: PyObjectId
    name: Optional[str]
    files: Optional[dict]
    status: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }
