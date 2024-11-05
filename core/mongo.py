import sys

from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient

from config import DB_NAME, MONGO_DB_URI

from ..logging import LOGGER

try:
    _mongo_async_ = _mongo_client_(MONGO_DB_URI)
    mongodb = _mongo_async_[DB_NAME]
    _mongo_sync_ = MongoClient(MONGO_DB_URI)
    pymongodb = _mongo_sync_[DB_NAME]
except Exception as e:
    LOGGER(__name__).error(f"Silahkan isi MONGO_DB_URI dan DB_NAME {e}")
    sys.exit(1)
