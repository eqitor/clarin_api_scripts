from app.clarinAPI.TagerAPI import FileTask
from time import sleep

task = FileTask("example.zip")
while not task.is_ready():
    print(task.get_progress())
    sleep(0.1)
task.download_and_save_file(out_file="resultat.zip")

