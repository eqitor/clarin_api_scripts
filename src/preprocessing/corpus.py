from zipfile import ZipFile
import re
import json


class Corpus:
    def __init__(self, source_zip):
        self.zip_file: ZipFile = ZipFile(source_zip)
        self.metadata: dict = self._load_metadata()

    def run_analysis(self):
        pass

    def _load_metadata(self):
        try:
            with self.zip_file.open('metadata.json') as metadata:
                result = json.load(metadata)
        except KeyError:
            raise FileNotFoundError("metadata.json does not exist in archive")
        return result

    def _get_documents_from_json(self):

        return []
