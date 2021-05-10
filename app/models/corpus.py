from mongoengine import Document, StringField, ObjectIdField, DictField
from typing import Optional


class Corpus(Document):
    name: str = StringField()
    files: dict = DictField()
    status: str = StringField(default="PROCESSING")
