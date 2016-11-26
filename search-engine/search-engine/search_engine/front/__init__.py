import logging

from flask import Flask
from elasticsearch import Elasticsearch
from pymongo import MongoClient

from search_engine import db, settings


logging.basicConfig(format='%(levelname)s\t%(asctime)s\t%(name)s\t%(message)s', datefmt='%H:%M:%S')


app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

mongo = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]
es = Elasticsearch(settings.ES_HOSTS, timeout=30)

links = db.LinkDAO(mongo)
texts = db.TextDAO(es)


import search_engine.front.profile
import search_engine.front.auth
