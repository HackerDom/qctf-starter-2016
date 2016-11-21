from elasticsearch import Elasticsearch
from pymongo import MongoClient

from search_engine import db, settings


def main():
    es = Elasticsearch(timeout=30)
    mongo = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]

    db.LinkDAO(mongo).setup()
    db.TextDAO(es).setup()

    print('Done')


if __name__ == '__main__':
    main()
