from time import sleep
from app.clarinAPI.TagerAPI import FileTask
import os
import asyncio


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

    def __init__(self, corpus_id):
        self.corpus_id = corpus_id
        self.zip_path = os.path.join('temp', str(corpus_id) + '.zip')
        if not os.path.isfile(self.zip_path):
            raise FileNotFoundError("Zip file of corpus does not exist")

    async def process_corpus(self):
        os.makedirs(os.path.join("temp", str(self.corpus_id)), exist_ok=True)
        for tool in self.clarin_tools:
            task = FileTask(self.zip_path, **self.clarin_tools[tool])
            await task.start_task()
            i = 0
            while not await task.is_ready():
                await asyncio.sleep(1)
                i += 1
                if i > 600:
                    raise TimeoutError(f"Corpus is processing too long for clarin tool: {tool}")
            else:
                file = os.path.join("temp", str(self.corpus_id), tool + ".zip")
                await task.download_and_save_file(out_file=file)
