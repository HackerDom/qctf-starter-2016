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
                "_default_": {
                    "properties": {
                        "text": {
                            "type": "string",
                            "analyzer": "russian",
                        },
                    },
                },
            },
        })

    _TYPE_PREFIX = 'user_'

    def save(self, user: str, url: str, texts: List[str]):
        es_requests = [{
            '_index': settings.ES_INDEX_NAME,
            '_type': TextDAO._TYPE_PREFIX + user,
            '_id': sha1(text.encode()).hexdigest(),  # Such ids guarantee fast maintenance of uniqueness
            'url': url,
            'user': user,
            'text': text,
        } for text in texts]
        elasticsearch.helpers.bulk(self._es, es_requests)

    def search(self, user: str, query: str) -> List[dict]:
        body = {
            "query": {
                "match": {
                    "text": query
                }
            },
            "highlight": {
                "fields": {
                    "text": {}
                }
            }
        }
        result = self._es.search(index='messages', doc_type=TextDAO._TYPE_PREFIX + user, body=body, size=20)
        return result['hits']['hits']
