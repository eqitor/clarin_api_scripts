import mongoengine as me
from pymongo import MongoClient

client: MongoClient = me.connect("db",
                                 host="mongodb",
                                 port=27017,
                                 username="root",
                                 password="example",
                                 authentication_source="admin")
