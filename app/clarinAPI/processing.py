from time import sleep
from app.clarinAPI.TagerAPI import FileTask
import os
import asyncio
import json
from zipfile import ZipFile
from app.clarinAPI.WordCounter import WordCounter
from aiohttp.client_exceptions import ServerDisconnectedError
import logging
from app.clarinAPI.Converter import Converter
from app.crud import corpus
from app.clarinAPI.NerAnalyzer import NerAnalyzer
from app.clarinAPI.TermoPL import TermoPL


class CorpusProcessing:
    clarin_tools = {
        "tager": {
            "option":
                "any2txt|wcrft2({\"guesser\":false, \"morfeusz2\":true})"
            },
        "ner": {
            "option":
                "any2txt|wcrft2|liner2({\"model\":\"top9\"})"
            },
        "termopl": {
            "option":
                "any2txt|wcrft2|dir|"
                "termopl2({\"mw\":true,\"sw\":\"/resources/termopl/termopl_sw.txt\","
                "\"cp\":\"/resources/termopl/termopl_cp.txt\"})"
            },
        "topics": {
            "option":
                "any2txt|div(20000)|wcrft2|"
                "fextor2({\"features\":\"base\",\"lang\":\"pl\",\"filters\":{\"base\":"
                "[{\"type\":\"pos_stoplist\",\"args\":{\"stoplist\":[\"subst\"],\"excluding\":false}}]}})"
                "|dir|feature2({\"filter\":{\"base\":{\"min_df\":2,\"max_df\":1,\"keep_n\":1000}}})"
                "|topic3({\"no_topics\":20,\"no_passes\":30,\"method\":\"artm_bigartm\",\"alpha\":-2,\"beta\":-0.01})"
                "|out(\"texts\")",
            "download_dict_list":
                ["value", "result", 0, "fileID"]
            }
    }

    def __init__(self, corpus_id : str):
        self.corpus_id = corpus_id
        self.zip_path = os.path.join('temp', str(corpus_id) + '.zip')
        if not os.path.isfile(self.zip_path):
            raise FileNotFoundError("Zip file of corpus does not exist")

    async def process_corpus(self):
        os.makedirs(os.path.join("temp", str(self.corpus_id)), exist_ok=True)
        timeout = 5
        for tool in self.clarin_tools:
            task = FileTask(self.zip_path, **self.clarin_tools[tool])
            await task.start_task()
            task_ready = False
            while not task_ready:
                try:
                    task_ready = await task.is_ready()
                except ServerDisconnectedError as e:
                    timeout = timeout * 2
                    logging.error(e.message)
                    logging.warning(f"timeout set to {timeout}")
                await asyncio.sleep(timeout)
            else:
                file = os.path.join("temp", str(self.corpus_id), tool + ".zip")
                await task.download_and_save_file(out_file=file)
                logging.warning(f"{tool} completed for corpus {self.corpus_id}")
                if tool == "tager":
                    await self.convert_zip_tagger(file)
                if tool == "ner":
                    await self.convert_zip_ner(file)
                if tool == "termopl":
                    await self.convert_zip_termopl(file)
        else:
            corpus.set_status(self.corpus_id, "READY")

    async def convert_zip_tagger(self, zip_file):
        converter = Converter()
        zf = ZipFile(zip_file)
        file_list = zf.namelist()
        dir_path = os.path.join("temp", self.corpus_id, "tager")
        dir_converted = os.path.join(dir_path, "converted")
        os.makedirs(dir_converted, exist_ok=True)
        zf.extractall(dir_path)
        for file in file_list:
            path = os.path.join(dir_path, file[:-4])
            with open(path, 'w') as out:
                filepath = os.path.join(dir_path, file)
                data = converter.convert(filepath)
                converted_path = os.path.join(dir_converted, file[:-4])
                with open(converted_path, 'w') as converted_out:
                    json.dump(data, converted_out)
                counted_words = WordCounter.count_words(data)
                json.dump(counted_words, out)


    async def convert_zip_ner(self, zip_file):
        zf = ZipFile(zip_file)
        file_list = zf.namelist()
        dir_path = os.path.join("temp", self.corpus_id, "ner")
        os.makedirs(dir_path, exist_ok=True)
        zf.extractall(dir_path)
        analyzer = NerAnalyzer()
        for file in file_list:
            path = os.path.join(dir_path, file[:-4])
            with open(path, 'w') as out:
                filepath = os.path.join(dir_path, file)
                ner_dict = analyzer.find_names(filepath)
                json.dump(ner_dict, out)


    async def convert_zip_termopl(self, zip_file):
        zf = ZipFile(zip_file)
        tager_dir_path = os.path.join("temp", self.corpus_id, "tager", "converted")
        file_list = os.listdir(tager_dir_path)
        dir_path = os.path.join("temp", self.corpus_id, "termopl")
        os.makedirs(dir_path, exist_ok=True)
        zf.extractall(dir_path)
        csv_path = os.path.join(dir_path, "dane", "terms.csv")
        converter = TermoPL(csv_path)
        termopl_dict = converter.get_data()
        for file in file_list:
            tager_path = os.path.join(tager_dir_path, file)
            out_path = os.path.join(dir_path, file)
            with open(tager_path, 'r') as tf:
                tager_dict = json.load(tf)
            termopl_list = self.get_termopl_for_file(tager_dict, termopl_dict)
            with open(out_path, 'w') as out:
                json.dump(termopl_list, out)

    def get_termopl_for_file(self, tager_list: list, termopl_dict: list) -> list:
        out = {}
        for i, tager in enumerate(tager_list):
            for termopl in termopl_dict:
                if tager['base'] == termopl['word'][0]:
                    if self.confirm_multiword(tager_list, i, termopl):
                        try:
                            out[termopl['original']]['count'] += 1
                        except KeyError:
                            out[termopl['original']] = termopl
                            out[termopl['original']]['count'] = 1
        return out

    def confirm_multiword(self, tager_list, index, termopl) -> bool:
        length = termopl['length']
        if length + index >= len(tager_list):
            return False
        for i in range(length):
            if termopl['word'][i] != tager_list[index + i]['base']:
                return False
        return True
