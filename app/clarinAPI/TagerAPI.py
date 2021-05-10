import requests
from requests import Response
import logging
import aiohttp
import asyncio
from aiofile import async_open
from aiohttp import ClientResponse
from app.core.config import settings



class FileTask:
    def __init__(self, file_path: str, option: str = 'any2txt|wcrft2({"guesser":false, "morfeusz2":true})',
                 download_dict_list=None):
        self._progress: float = 0
        self._download_url = ""
        if download_dict_list is None:
            self.download_dict_list = ["value", 0, "fileID"]
        else:
            self.download_dict_list = download_dict_list
        self._api = FileClarinAPI()
        self._remote_filepath = ""
        self._file_path = file_path
        self._task_id = None
        self._option: str = option

    async def start_task(self):
        self._remote_filepath = await self._api.upload_zip_file(self._file_path)
        self._option = f"filezip({self._remote_filepath})|" + self._option + "|dir|makezip"
        self._task_id = await self._api.start_processing(self._option)
        logging.warning(self._task_id)

    async def is_ready(self):
        body = await self._api.get_task_status(self._task_id)
        if body['status'] == 'DONE':
            self._progress = 1
            logging.warning(body)
            self._download_url = self._get_download_link(body)
            return True
        else:
            logging.warning(body)
            self._progress = body["value"]
            return False

    async def download_and_save_file(self, out_file):
        await self._api.download_task_result(self._download_url, out_file)

    def get_progress(self) -> float:
        return self._progress

    def _get_download_link(self, response: dict):
        result = response
        for key in self.download_dict_list:
            result = result[key]
        return result


class FileClarinAPI:
    """Class providing simple connection to nlprest2 API."""

    async def upload_zip_file(self, file_path):
        data = {'file': open(file_path, 'rb'),
                "Content-Disposition": "form-data; name=\"file\"; filename=\"korpus.zip\"",
                "Content-Type": "application/x-zip-compressed"}
        async with aiohttp.ClientSession() as session:
            response = await session.post("http://ws.clarin-pl.eu/nlprest2/base/upload/", data=data)
            path = await response.text()
        return path

    async def start_processing(self, options='any2txt|wcrft2({"guesser":false, "morfeusz2":true})') -> str:
        """Uploads file and starts processing. Returns Response object."""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/startTask"

        body = {
            "application": "ws.clarin-pl.eu",
            "lpmn": options,
            "user": 'demo'
        }
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, json=body)
            task_id = await response.text()
        return task_id

    async def get_task_status(self, task) -> dict:
        """Checks status of uploaded task."""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/getStatus/"
        full_url = url + task

        async with aiohttp.ClientSession() as session:
            async with session.get(full_url) as resp:
                body = await resp.json(content_type=None)
        return body

    async def download_task_result(self, download_path, output_path):
        """Downloads XML document with task processing results.
        IMPORTANT: Remember to put result file ID as task (str or Response object)"""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/download"  # don't add / at the end!
        full_url = url + download_path

        async with async_open(output_path, "wb") as f:
            async with aiohttp.ClientSession() as session:
                async with session.get(full_url) as resp:
                    data = await resp.read()
                    await f.write(data)
        return
