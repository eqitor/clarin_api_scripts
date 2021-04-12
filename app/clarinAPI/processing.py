from app.clarinAPI import Task
from time import sleep
import pandas as pd




class CorpusProcessing:
    def __init__(self, documents: list, options: list):
        self.documents = documents
        self.options = options
        self.results = pd.DataFrame(columns=["doc", "opt", "result"])

    def process_corpus(self):
        # TODO documents moze byc zipem czy coś, trzeba dogadać
        # TODO options to tez moze byc obiekt jakiejs klasy z opcjami ktore maja przeleciec dla dokumentow
        for doc in self.documents:
            for opt in self.options:
                result = self._process_document(doc, opt)
                self.results = self.results.append(
                    {"doc": doc, "opt": opt, "result": result},
                    ignore_index=True)
        return self.results

    def _process_document(self, text:str, option:str) -> str:
        task = Task(text, option)
        while not task.is_ready():
            print(task.get_progress())
            sleep(1)
        result = task.download_file()
        if result.status_code != 200:
            raise ConnectionError(f"Document was not processed correctly: {result.text}")
        return result.text
