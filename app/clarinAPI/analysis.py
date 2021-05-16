from app.crud import corpus
import os, json, logging
from operator import itemgetter


class TagerAnalysis:

    default_ctags = {
        'subst', 'adj', 'adv'
    }

    def __init__(self, corpus_id: str):
        self.corpus_id = corpus_id
        self.corpus = corpus.get(corpus_id)
        self.metadata = self.corpus.files
        self.ctags = self.default_ctags

    def get_analysis(self, ctags=None, limit=None):
        if ctags is not None:
            self.ctags = ctags
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
        analysis_list = []
        for key, value in analysis_dict.items():
            new_dict = self._convert_key_value_to_no_key(key,value)
            if new_dict["speech"] in self.ctags:
                analysis_list.append(new_dict)
        sorted_list = sorted(analysis_list, key=itemgetter('count'), reverse=True)
        if limit is None:
            return sorted_list
        else:
            return sorted_list[:limit]


    def _convert_key_value_to_no_key(self,key,value) -> dict:
        try:
            word, ctag = key.split(" ")
        except ValueError:
            logging.error(f"There is space in a word!!!: {key}")
            splitted = key.split(" ")
            word = str.join(" ", splitted[:-1])
            ctag = splitted[-1]
        new_dict = {
            "word": word,
            "speech": ctag,
            "count": value
        }
        return new_dict