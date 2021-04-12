from app.models import Corpus
from app.schemas import CorpusCreate
from typing import Optional

class CRUDCorpus:

    def create(self, obj_in:CorpusCreate) -> Corpus:
        db_obj = Corpus(
            name=obj_in.name
        )
        db_obj = db_obj.save()
        return db_obj

    def get_by_name(self, name: str) -> Optional[Corpus]:
        obj_out = Corpus.objects(name=name).first()
        return obj_out


corpus = CRUDCorpus()
