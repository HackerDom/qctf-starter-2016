from datetime import datetime
from hashlib import sha1
from typing import List, Optional

import pymongo


__all__ = ['LinkDAO']


class LinkDAO:
    def __init__(self, mongo):
        self._collection = mongo.links

    def setup(self):
        self._collection.create_index([
            ('distance', pymongo.ASCENDING),
            ('add_time', pymongo.ASCENDING),
        ])

    def select_next(self) -> Optional[dict]:
        return self._collection.find_one_and_delete({}, sort=[
            ('distance', pymongo.ASCENDING),
            ('add_time', pymongo.ASCENDING),
        ])

    def save(self, user: str, links: List[str], distance: int):
        requests = [pymongo.UpdateOne({
            '_id': sha1((user + '$' + url).encode()).digest(),  # Such ids guarantee fast maintenance of uniqueness
        }, {
            '$min': {
                'distance': distance,
            },
            '$setOnInsert': {
                'add_time': datetime.utcnow(),
                'url': url,
                'user': user,
            },
        }, upsert=True) for url in links]
        self._collection.bulk_write(requests, ordered=False)