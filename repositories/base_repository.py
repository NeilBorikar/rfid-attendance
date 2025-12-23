from typing import Any, Dict, List, Optional
from pymongo.collection import Collection
from bson import ObjectId


class BaseRepository:
    """
    Base repository providing common MongoDB operations.
    """

    def __init__(self, collection: Collection):
        self.collection = collection

    def find_one(self, query: Dict[str, Any]) -> Optional[Dict]:
        return self.collection.find_one(query)

    def find_many(self, query: Dict[str, Any]) -> List[Dict]:
        return list(self.collection.find(query))

    def insert_one(self, document: Dict[str, Any]) -> ObjectId:
        result = self.collection.insert_one(document)
        return result.inserted_id

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        result = self.collection.update_one(query, {"$set": update})
        return result.modified_count > 0

    def exists(self, query: Dict[str, Any]) -> bool:
        return self.collection.count_documents(query, limit=1) > 0
