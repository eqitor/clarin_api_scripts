import os
from time import sleep
from app.clarinAPI.TagerAPI import FileTask


#@pytest.mark.skip(reason="higher level tests already check this functionality")
class Test_FileTask():

    def setup(self):
        self.task = FileTask("example.zip")

    def test_check_progress(self):
        result = self.task.is_ready()
        if result:
            assert type(self.task.get_progress()) == str
            assert self.task.get_progress() != ""
        else:
            assert self.task.get_progress() < 1


    def test_download_result(self):
        i = 0
        while not self.task.is_ready():
            sleep(0.1)
            i += 1
            if i > 600:
                assert False
        else:
            file = "resultat.zip"
            self.task.download_and_save_file(out_file=file)
            assert os.path.isfile(file)
