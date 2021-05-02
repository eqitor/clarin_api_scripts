from app.crud import corpus
import os, json, logging

class TagerAnalysis:

    def __init__(self, corpus_id: str):
        self.corpus_id = corpus_id
        self.corpus = corpus.get(corpus_id)
        self.metadata = self.corpus.files

    def get_analysis(self):
        analysis_dict = {}
        for file in self.metadata:
            path = os.path.join("temp", self.corpus_id, "tager", file)
            with open(path, "r") as f:
                data = json.load(f)
                logging.warning(data)
                for word in data:
                    try:
                        analysis_dict[word] += data[word]
                    except KeyError:
                        analysis_dict[word] = data[word]
        return analysis_dict
