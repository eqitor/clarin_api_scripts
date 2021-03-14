import requests

class TagerAPI:
    """Class providing simple connection to nlprest2 API."""

    def send_GET(self, url, task):
        """Sends GET request for given URL and task."""
        if type(task) is requests.models.Response:
            task = task.text

        full_url = url + task
        request_response = requests.get(full_url)

        return request_response

    def start_processing(self, text):
        """Uploads file and starts processing. Returns Response object."""
        url = r"http://ws.clarin-pl.eu/nlprest2/base/startTask"
        body = {
            "lpmn": 'any2txt|wcrft2({"guesser":false, "morfeusz2":true})',
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




