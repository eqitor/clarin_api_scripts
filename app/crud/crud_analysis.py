from app.models import Analysis
from app.schemas import AnalysisCreate
from app import schemas
from typing import Optional
import logging

class CRUDAnalysis:

    def create(self, obj_in: AnalysisCreate) -> schemas.Analysis:
        logging.warning(obj_in)
        db_obj = Analysis(
            boundaries=obj_in.boundaries,
            corpus_id=obj_in.corpus_id,
            options=obj_in.options
        )
        db_obj = db_obj.save()
        logging.warning(str(db_obj.id))
        logging.warning(db_obj.to_json())
        # TODO from_mongo, to_mongo
        return db_obj

    def get(self, id: str) -> Optional[Analysis]:
        obj_out = Analysis.objects(id=id).first()
        return obj_out

    def set_status(self, id:str, status: str) -> None:
        analysis = self.get(id)
        analysis.update(status=status)

    def set_files(self, id:str, files: list) -> None:
        analysis = self.get(id)
        analysis.update(files=files)
        analysis.update(files_count=len(files))

    def set_result(self, id:str, result: dict) -> None:
        analysis = self.get(id)
        analysis.update(result=result)


analysis = CRUDAnalysis()
