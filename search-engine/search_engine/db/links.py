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
        return self._collection.find_one_and_update({}, sort=[
            ('distance', pymongo.ASCENDING),
            ('add_time', pymongo.ASCENDING),
        ], update={
            'status': 'processing',
        })

    @staticmethod
    def _get_id(user: str, url: str) -> bytes:
        # Such ids guarantee fast maintenance of uniqueness
        return sha1((user + '$' + url).encode()).digest()

    def save(self, user: str, links: List[str], distance: int, *, force_status: bool):
        requests = []
        for url in links:
            body = {
                '$min': {
                    'distance': distance,
                },
                '$setOnInsert': {
                    'url': url,
                    'user': user,
                },
            }
            body['$set' if force_status else '$setOnInsert'].update({
                'add_time': datetime.utcnow(),
                'status': 'queued',
            })

            requests.append(pymongo.UpdateOne({'_id': LinkDAO._get_id(user, url)}, body, upsert=True))
        self._collection.bulk_write(requests, ordered=False)

    def update_status(self, user: str, url: str, status: str, *, reason: str=None):
        body = {'status': status}
        if reason is not None:
            body['status_reason'] = reason

        self._collection.update_one({'_id': LinkDAO._get_id(user, url)}, body)
