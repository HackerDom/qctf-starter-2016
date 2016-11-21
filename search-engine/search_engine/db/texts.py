from hashlib import sha1
from typing import List

import elasticsearch.helpers
from elasticsearch import Elasticsearch

from search_engine import settings


__all__ = ['TextDAO']


class TextDAO:
    def __init__(self, es: Elasticsearch):
        self._es = es

    def setup(self):
        self._es.indices.create(index=settings.ES_INDEX_NAME, body={
            "mappings": {
                "texts": {
                    "properties": {
                        "text": {
                            "type": "string",
                            "analyzer": "russian",
                        },
                    },
                },
            },
        })

    def save(self, user: str, url: str, texts: List[str]):
        es_requests = [{
            '_index': settings.ES_INDEX_NAME,
            '_type': 'texts',
            '_id': sha1((user + '$' + text).encode()).hexdigest(),  # Such ids guarantee fast maintenance of uniqueness
            'url': url,
            'user': user,
            'text': text,
        } for text in texts]
        elasticsearch.helpers.bulk(self._es, es_requests)