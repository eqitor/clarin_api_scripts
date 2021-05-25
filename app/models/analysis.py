from mongoengine import *
from typing import Optional


class Analysis(Document):
    files: list = ListField()
    status: str = StringField(default="PROCESSING")
    boundaries: dict = DictField()
    options: dict = DictField()
    corpus_id: str = StringField()
