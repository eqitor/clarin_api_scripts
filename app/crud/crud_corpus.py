from app.models import Corpus
from app.schemas import CorpusCreate
from app import schemas
from typing import Optional
import logging

class CRUDCorpus:

    def create(self, obj_in: CorpusCreate) -> schemas.Corpus:
        logging.warning(obj_in)
        db_obj = Corpus(
            name=obj_in.name,
            files=obj_in.files
        )
        db_obj = db_obj.save()
        logging.warning(str(db_obj.id))
        logging.warning(db_obj.to_json())
        # TODO from_mongo, to_mongo
        return db_obj

    def get(self, id: str) -> Optional[Corpus]:
        obj_out = Corpus.objects(id=id).first()
        return obj_out

    def get_by_name(self, name: str) -> Optional[Corpus]:
        obj_out = Corpus.objects(name=name).first()
        return obj_out

    def set_status(self, id:str, status:str) -> None:
        corpus = self.get(id)
        corpus.update(status=status)

corpus = CRUDCorpus()
