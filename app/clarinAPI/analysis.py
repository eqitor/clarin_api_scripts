from app.crud import corpus
from app import crud
import os, json, logging
from operator import itemgetter
from app.clarinAPI.filtering import Filtering

class Analysis:
    def __init__(self, corpus_id: str, boundaries: dict, analysis_id: str):
        filtr = Filtering()
        self.corpus_id = corpus_id
        self.analysis_id = analysis_id
        self.corpus = corpus.get(corpus_id)
        self.metadata = self.corpus.files
        self.boundaries = boundaries
        self.files = filtr.get_list_of_files_for_filters(self.metadata, boundaries, self.corpus.filters)
        crud.analysis.set_files(self.analysis_id, self.files)

    async def start_analysis(self):
        ta = TagerAnalysis(self.analysis_id)
        tagger = ta.get_analysis()
        na = NerAnalysis(self.analysis_id)
        ner = na.get_analysis()
        tpla = TermoPLAnalysis(self.analysis_id)
        termopl = tpla.get_analysis()
        result = {"tagger": tagger, "ner": ner, "termopl": termopl}
        crud.analysis.set_result(self.analysis_id, result)
        crud.analysis.set_status(self.analysis_id, "DONE")


class TagerAnalysis:
    default_ctags = {
        'subst', 'adj', 'adv'
    }

    def __init__(self, analysis_id: str):
        self.analysis = crud.analysis.get(analysis_id)
        self.corpus_id = self.analysis.corpus_id
        self.files = self.analysis.files

    def get_analysis(self,  limit=None, ctags=None):
        if ctags is None:
            ctags = self.default_ctags
        analysis_dict = {}
        for file in self.files:
            path = os.path.join("temp", self.corpus_id, "tager", file)
            with open(path, "r") as f:
                data = json.load(f)
                for word in data:
                    try:
                        analysis_dict[word] += data[word]
                    except KeyError:
                        analysis_dict[word] = data[word]
        analysis_list = []
        for key, value in analysis_dict.items():
            new_dict = self._convert_key_value_to_no_key(key,value)
            if new_dict["speech"] in ctags:
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

class NerAnalysis:

    def __init__(self, analysis_id: str):
        self.analysis_id = analysis_id
        self.analysis = crud.analysis.get(analysis_id)
        self.files = self.analysis.files
        self.corpus_id = self.analysis.corpus_id

    def get_analysis(self, limit=None):
        analysis_dict = {}
        for file in self.files:
            path = os.path.join("temp", self.corpus_id, "ner", file)
            with open(path, "r") as f:
                data = json.load(f)
                self._merge_ner_dicts(data, analysis_dict)
        analysis_list = list(analysis_dict.values())
        sorted_list = sorted(analysis_list, key=itemgetter('count'), reverse=True)
        if limit is None:
            return sorted_list
        else:
            return sorted_list[:limit]

    def _merge_ner_dicts(self, dict_from: dict, dict_to: dict):
        for base in dict_from:
            if base in dict_to:
                dict_to[base]['count']+=dict_from[base]['count']
                unique_word_list = [x for x in dict_from[base]['word'] if x not in dict_to[base]['word']]
                dict_to[base]['word'] += unique_word_list
                dict_to[base]['speech'] += dict_from[base]['speech']
            else:
                dict_to[base] = dict_from[base]
        return dict_to

class TermoPLAnalysis:

    def __init__(self, analysis_id: str):
        self.analysis = crud.analysis.get(analysis_id)
        self.corpus_id = self.analysis.corpus_id
        self.files = self.analysis.files

    def get_analysis(self,  limit=None):
        analysis_dict = {}
        for file in self.files:
            path = os.path.join("temp", self.corpus_id, "termopl", file)
            with open(path, "r") as f:
                data = json.load(f)
                for termopl in data:
                    try:
                        analysis_dict[termopl]['count'] += data[termopl]['count']
                    except KeyError:
                        analysis_dict[termopl] = data[termopl]
        analysis_list = list(analysis_dict.values())
        sorted_list = sorted(analysis_list, key=itemgetter('count'), reverse=True)
        if limit is None:
            return sorted_list
        else:
            return sorted_list[:limit]
