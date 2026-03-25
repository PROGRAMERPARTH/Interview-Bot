from pymongo import MongoClient

from app.core.config import settings


_client = MongoClient(settings.mongodb_uri)
_db = _client[settings.mongodb_db]


def get_db():
    return _db
