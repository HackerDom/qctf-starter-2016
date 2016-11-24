import logging
from threading import Thread

from elasticsearch import Elasticsearch
from pymongo import MongoClient

from search_engine import db, settings
from search_engine.crawler.crawler import Crawler


logging.basicConfig(format='%(levelname)s\t%(asctime)s\t%(name)s\t%(message)s', datefmt='%H:%M:%S')


def main():
    es = Elasticsearch(timeout=30)
    mongo = MongoClient(settings.MONGO_URI)[settings.MONGO_DB_NAME]

    links = db.LinkDAO(mongo)
    texts = db.TextDAO(es)

    threads = [Thread(target=Crawler('crawler-{}'.format(i), links, texts).run)
               for i in range(settings.CRAWLER_THREADS)]
    for item in threads:
        item.start()
    for item in threads:
        item.join()


if __name__ == '__main__':
    main()
