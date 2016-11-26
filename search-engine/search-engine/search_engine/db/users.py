from typing import Optional


__all__ = ['UserDAO']


class UserDAO:
    def __init__(self, mongo):
        self._collection = mongo.users

    def register(self, user: dict) -> bool:
        result = self._collection.update_one({'_id': user['_id']}, {'$setOnInsert': user}, upsert=True)
        return result.upserted_id is not None

    def find(self, username: str) -> Optional[dict]:
        return self._collection.find_one({'_id': username})
