from mongoengine import Document, StringField, ObjectIdField
from typing import Optional


class Corpus(Document):
    name: str = StringField()

