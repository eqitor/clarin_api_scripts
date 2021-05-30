from app.clarinAPI.TagerAPI import FileTask
from time import sleep
from zipfile import ZipFile
from random import randint
import json
from datetime import datetime

# task = FileTask("example.zip")
# while not task.is_ready():
#     print(task.get_progress())
#     sleep(0.1)
# task.download_and_save_file(out_file="resultat.zip")
#

dates = ["2020-10-19", "2020-5-10", "2021-03-02", "2020-8-30"]
strings = ["pwr", "onet", "wp", "wyborcza"]
zf = ZipFile("example.zip")
files = zf.namelist()
metadata = {}
for file in files:
    metadata[file[:-4]] = {"filter1": randint(0, 4), "filter2": strings[randint(0, 3)], "filter3": dates[randint(0, 3)]}

with open("metadata.json", "w") as md:
    json.dump(metadata, md)
