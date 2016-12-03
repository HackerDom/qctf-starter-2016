from hashlib import sha1

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
        }, ignore=400)  # Ignore IndexAlreadyExistsException

    _TYPE_PREFIX = 'user_'

    def save(self, username: str, url: str, title: str, text: str):
        body = {
            'title': title,
            'text': text,
            'url': url,
        }
        self._es.index(index=settings.ES_INDEX_NAME, doc_type=TextDAO._TYPE_PREFIX + username,
                       id=sha1(url.encode()).hexdigest(), body=body)

    def delete_by_user(self, username: str):
        self._es.delete_by_query(index=settings.ES_INDEX_NAME, doc_type=TextDAO._TYPE_PREFIX + username, body={})

    def search(self, username: str, query: str) -> dict:
        body = {
            "query": {
                "match": {
                    "text": query
                }
            },
            "highlight": {
                "fields": {
                    "text": {
                        "fragment_size": 150
                    }
                }
            }
        }
        result = self._es.search(index=settings.ES_INDEX_NAME, doc_type=TextDAO._TYPE_PREFIX + username,
                                 body=body, size=20)
        return result['hits']
