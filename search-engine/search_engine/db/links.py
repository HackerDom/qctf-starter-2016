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
            ('status', pymongo.ASCENDING),
            ('distance', pymongo.ASCENDING),
            ('add_time', pymongo.ASCENDING),
        ])
        self._collection.create_index([
            ('username', pymongo.ASCENDING),
            ('add_time', pymongo.DESCENDING),
        ])

    def select_next(self) -> Optional[dict]:
        return self._collection.find_one_and_update({
            'status': 'queued',
        }, sort=[
            ('distance', pymongo.ASCENDING),
            ('add_time', pymongo.ASCENDING),
        ], update={
            '$set': {
                'status': 'processing',
            },
        })

    @staticmethod
    def _get_id(username: str, url: str) -> bytes:
        return sha1((username + '$' + url).encode()).digest()[:12]

    def save(self, username: str, links: List[str], distance: int, *, force_status: bool):
        requests = []
        for url in links:
            body = {
                '$min': {
                    'distance': distance,
                },
                '$setOnInsert': {
                    'url': url,
                    'username': username,
                },
            }
            status_set_body = {
                'add_time': datetime.utcnow(),
                'status': 'queued',
            }
            if force_status:
                body['$set'] = status_set_body
            else:
                body['$setOnInsert'].update(status_set_body)

            requests.append(pymongo.UpdateOne({'_id': LinkDAO._get_id(username, url)}, body, upsert=True))
        if requests:
            self._collection.bulk_write(requests, ordered=False)

    def update_status(self, username: str, url: str, status: str, *, reason: str=None):
        body = {
            '$set': {
                'status': status,
            },
        }
        if reason is not None:
            body['$set']['status_reason'] = reason

        self._collection.update_one({'_id': LinkDAO._get_id(username, url)}, body)

    def get_by_user(self, username: str) -> List[dict]:
        return self._collection.find({'username': username}, sort=[('add_time', pymongo.DESCENDING)])
