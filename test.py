from app.clarinAPI.TagerAPI import FileTask
from time import sleep
from zipfile import ZipFile
from random import randint
import json

# task = FileTask("example.zip")
# while not task.is_ready():
#     print(task.get_progress())
#     sleep(0.1)
# task.download_and_save_file(out_file="resultat.zip")
#

zf = ZipFile("example.zip")
files = zf.namelist()
metadata = {}
for file in files:
    metadata[file[:-4]] = {"filter1": randint(0, 4), "filter2": "pwr"}

with open("metadata.json", "w") as md:
    json.dump(metadata, md)


