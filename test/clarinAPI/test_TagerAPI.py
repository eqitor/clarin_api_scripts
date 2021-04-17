import os
from time import sleep
from app.clarinAPI.TagerAPI import FileTask
import pytest
import asyncio


#@pytest.mark.skip(reason="higher level tests already check this functionality")
class Test_FileTask():

    def setup(self):
        self.task = FileTask("example.zip")
        asyncio.run(self.task.start_task())

    @pytest.mark.asyncio
    async def test_check_progress(self):
        result = await self.task.is_ready()
        if result:
            assert type(self.task.get_progress()) == str
            assert self.task.get_progress() != ""
        else:
            assert self.task.get_progress() < 1

    @pytest.mark.asyncio
    async def test_download_result(self):
        i = 0
        while not await self.task.is_ready():
            sleep(0.1)
            i += 1
            if i > 600:
                assert False
        else:
            file = "resultat.zip"
            await self.task.download_and_save_file(out_file=file)
            assert os.path.isfile(file)
