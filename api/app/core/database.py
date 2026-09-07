import os
import json
import asyncio
from typing import Dict, Any, List, Optional
import motor.motor_asyncio
from app.core.config import settings

class AsyncMemoryCollection:
    """High-fidelity async MongoDB-compatible collection for standalone local execution and tests."""
    def __init__(self, name: str, file_path: str):
        self.name = name
        self.file_path = file_path
        self._data: List[Dict[str, Any]] = []
        self._lock = asyncio.Lock()
        self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = []
        else:
            self._data = []

    def _save(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, default=str)

    async def insert_one(self, doc: Dict[str, Any]):
        async with self._lock:
            doc_copy = dict(doc)
            if "id" not in doc_copy and "_id" not in doc_copy:
                import uuid
                doc_copy["id"] = str(uuid.uuid4())
            self._data.append(doc_copy)
            self._save()
            return type("InsertResult", (), {"inserted_id": doc_copy.get("id") or doc_copy.get("_id")})

    async def find_one(self, filter_query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        async with self._lock:
            for item in self._data:
                match = True
                for k, v in filter_query.items():
                    if k == "_id" and "_id" not in item and "id" in item:
                        if item["id"] != v:
                            match = False
                            break
                    elif item.get(k) != v:
                        match = False
                        break
                if match:
                    return dict(item)
            return None

    async def find(self, filter_query: Optional[Dict[str, Any]] = None, sort_by: Optional[str] = None, ascending: bool = True) -> List[Dict[str, Any]]:
        async with self._lock:
            filter_query = filter_query or {}
            results = []
            for item in self._data:
                match = True
                for k, v in filter_query.items():
                    if item.get(k) != v:
                        match = False
                        break
                if match:
                    results.append(dict(item))
            if sort_by:
                results.sort(key=lambda x: x.get(sort_by, 0), reverse=not ascending)
            return results

    async def update_one(self, filter_query: Dict[str, Any], update_doc: Dict[str, Any], upsert: bool = False):
        async with self._lock:
            target = None
            for item in self._data:
                match = True
                for k, v in filter_query.items():
                    if item.get(k) != v:
                        match = False
                        break
                if match:
                    target = item
                    break

            if target is not None:
                if "$set" in update_doc:
                    target.update(update_doc["$set"])
                else:
                    target.update(update_doc)
                self._save()
                return type("UpdateResult", (), {"matched_count": 1, "modified_count": 1})
            elif upsert:
                new_item = dict(filter_query)
                if "$set" in update_doc:
                    new_item.update(update_doc["$set"])
                else:
                    new_item.update(update_doc)
                self._data.append(new_item)
                self._save()
                return type("UpdateResult", (), {"matched_count": 0, "modified_count": 1, "upserted_id": new_item.get("id")})
            return type("UpdateResult", (), {"matched_count": 0, "modified_count": 0})

    async def count_documents(self, filter_query: Optional[Dict[str, Any]] = None) -> int:
        res = await self.find(filter_query)
        return len(res)

    async def delete_many(self, filter_query: Dict[str, Any]):
        async with self._lock:
            new_data = []
            deleted = 0
            for item in self._data:
                match = True
                for k, v in filter_query.items():
                    if item.get(k) != v:
                        match = False
                        break
                if not match:
                    new_data.append(item)
                else:
                    deleted += 1
            self._data = new_data
            self._save()
            return type("DeleteResult", (), {"deleted_count": deleted})


class AsyncMongoCollectionWrapper:
    """
    Transparent wrapper for Motor async MongoDB collection.
    Ensures that find(), find_one(), insert_one(), update_one(), count_documents(), and delete_many()
    provide identical calling conventions to AsyncMemoryCollection across the entire platform.
    """
    def __init__(self, motor_collection):
        self._col = motor_collection

    async def insert_one(self, doc: Dict[str, Any]):
        doc_copy = dict(doc)
        if "id" not in doc_copy and "_id" not in doc_copy:
            import uuid
            doc_copy["id"] = str(uuid.uuid4())
        res = await self._col.insert_one(doc_copy)
        return type("InsertResult", (), {"inserted_id": doc_copy.get("id") or str(res.inserted_id)})

    async def find_one(self, filter_query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Normalize _id / id queries
        q = dict(filter_query)
        res = await self._col.find_one(q)
        if res and "_id" in res and "id" not in res:
            res["id"] = str(res["_id"])
        return res

    async def find(self, filter_query: Optional[Dict[str, Any]] = None, sort_by: Optional[str] = None, ascending: bool = True) -> List[Dict[str, Any]]:
        cursor = self._col.find(filter_query or {})
        if sort_by:
            cursor = cursor.sort(sort_by, 1 if ascending else -1)
        docs = await cursor.to_list(length=2000)
        for d in docs:
            if "_id" in d and "id" not in d:
                d["id"] = str(d["_id"])
        return docs

    async def update_one(self, filter_query: Dict[str, Any], update_doc: Dict[str, Any], upsert: bool = False):
        res = await self._col.update_one(filter_query, update_doc, upsert=upsert)
        return type("UpdateResult", (), {
            "matched_count": res.matched_count,
            "modified_count": res.modified_count,
            "upserted_id": res.upserted_id
        })

    async def count_documents(self, filter_query: Optional[Dict[str, Any]] = None) -> int:
        return await self._col.count_documents(filter_query or {})

    async def delete_many(self, filter_query: Dict[str, Any]):
        res = await self._col.delete_many(filter_query)
        return type("DeleteResult", (), {"deleted_count": res.deleted_count})


class DatabaseManager:
    def __init__(self):
        self.motor_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
        self.db = None
        self.is_atlas = False
        self._collections: Dict[str, Any] = {}

    async def connect(self):
        if settings.MONGODB_URI:
            try:
                self.motor_client = motor.motor_asyncio.AsyncIOMotorClient(
                    settings.MONGODB_URI,
                    serverSelectionTimeoutMS=3000
                )
                await self.motor_client.server_info()
                self.db = self.motor_client[settings.DATABASE_NAME]
                self.is_atlas = True
                print(f"Connected successfully to MongoDB: {settings.DATABASE_NAME}")
                return
            except Exception as e:
                print(f"MongoDB connection unavailable ({e}). Initializing high-reliability local store.")
        
        # Fallback to local high-fidelity persistence
        self.is_atlas = False
        os.makedirs("data/db", exist_ok=True)
        print("Initialized local database engine at data/db/")

    def get_collection(self, name: str):
        if self.is_atlas and self.db is not None:
            if name not in self._collections:
                self._collections[name] = AsyncMongoCollectionWrapper(self.db[name])
            return self._collections[name]
        if name not in self._collections:
            path = os.path.join("data", "db", f"{name}.json")
            self._collections[name] = AsyncMemoryCollection(name, path)
        return self._collections[name]

    async def close(self):
        if self.motor_client:
            self.motor_client.close()

db_manager = DatabaseManager()

