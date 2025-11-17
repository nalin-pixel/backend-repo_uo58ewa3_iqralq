from typing import Any, Dict, List, Optional
from datetime import datetime
import os
from pymongo import MongoClient
from pymongo.collection import Collection

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: Optional[MongoClient] = None
_db = None


def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db


def collection(name: str) -> Collection:
    return get_db()[name]


def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow()
    data["created_at"] = data.get("created_at", now)
    data["updated_at"] = data.get("updated_at", now)
    col = collection(collection_name)
    result = col.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 100) -> List[Dict[str, Any]]:
    col = collection(collection_name)
    cursor = col.find(filter_dict or {}).limit(limit).sort("created_at", -1)
    items: List[Dict[str, Any]] = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])  # stringify ObjectId
        items.append(doc)
    return items
