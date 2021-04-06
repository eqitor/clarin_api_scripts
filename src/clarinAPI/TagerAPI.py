import requests
from requests import Response


class FileTask:
    def __init__(self, file: str, options: str = 'any2txt|wcrft2({"guesser":false, "morfeusz2":true})'):
        self._progress: float = 0
        self._download_url = ""
        self._api = FileTagerAPI()
        self._task_id = self._api.start_processing(file, options).text

    def is_ready(self):
        resp = self._api.get_task_status(self._task_id)
        if resp.json()['status'] == 'DONE':
            self._progress = 1
            self._download_url = resp.json()["value"][0]["fileID"]
            print(resp.text)
            return True
        else:
            print(resp.text)
            self._progress = resp.json()["value"]

    def get_progress(self) -> float:
        return self._progress

    def download_file(self):
        return self._api.download_task_result(self._download_url)



class Task:
    def __init__(self, text: str, options: str = 'any2txt|wcrft2({"guesser":false, "morfeusz2":true})'):
        self._progress: float = 0
        self._download_url = ""
        self._api = TagerAPI()
        self._task_id = self._api.start_processing(text, options).text

    def is_ready(self):
        resp = self._api.get_task_status(self._task_id)
        if resp.json()['status'] == 'DONE':
            self._progress = 1
            self._download_url = resp.json()["value"][0]["fileID"]
            return True
        else:
            self._progress = resp.json()["value"]

    def get_progress(self) -> float:
        return self._progress

    def download_file(self):
        return self._api.download_task_result(self._download_url)


class FileTagerAPI:
    """Class providing simple connection to nlprest2 API."""

    def send_GET(self, url, task):
        """Sends GET request for given URL and task."""
        if type(task) is requests.models.Response:
            task = task.text

        full_url = url + task
        print(full_url)
        request_response = requests.get(full_url)

        return request_response

    def start_processing(self, file, options ='any2txt|wcrft2({"guesser":false, "morfeusz2":true})') -> Response:
        """Uploads file and starts processing. Returns Response object."""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/startTask"

        body = {
            "application": "ws.clarin-pl.eu",
            "lpmn": options,
            "user": 'demo'
        }
        print(body)
        request_response = requests.post(url, json=body)

        return request_response

    def get_task_status(self, task):
        """Checks status of uploaded task."""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/getStatus/"
        request_response = self.send_GET(url, task)

        return request_response

    def download_task_result(self, task):
        """Downloads XML document with task processing results.
        IMPORTANT: Remember to put result file ID as task (str or Response object)"""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/download"  # don't add / at the end!
        request_response = self.send_GET(url, task)

        return request_response

    def get_result_id(self, status_response):
        """Fetches processing results ID from task status response."""
        return status_response.json()["value"][0]["fileID"]


class TagerAPI:
    """Class providing simple connection to nlprest2 API."""

    def send_GET(self, url, task):
        """Sends GET request for given URL and task."""
        if type(task) is requests.models.Response:
            task = task.text

        full_url = url + task
        request_response = requests.get(full_url)

        return request_response

    def start_processing(self, text, options ='any2txt|wcrft2({"guesser":false, "morfeusz2":true})') -> Response:
        """Uploads file and starts processing. Returns Response object."""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/startTask"
        body = {
            "lpmn": options,
            "text": text,
            "user": 'demo'
        }

        request_response = requests.post(url, json=body)

        return request_response

    def get_task_status(self, task):
        """Checks status of uploaded task."""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/getStatus/"
        request_response = self.send_GET(url, task)
        return request_response

    def download_task_result(self, task):
        """Downloads XML document with task processing results.
        IMPORTANT: Remember to put result file ID as task (str or Response object)"""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/download"  # don't add / at the end!
        request_response = self.send_GET(url, task)
        return request_response

    def get_result_id(self, status_response):
        """Fetches processing results ID from task status response."""
        return status_response.json()["value"][0]["fileID"]
