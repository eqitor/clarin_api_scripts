from mongoengine import Document, StringField


class Corpus(Document):
    name = StringField()

