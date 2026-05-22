import os
import json
from typing import List, Dict, Optional, Any
import numpy as np
from datetime import datetime, timezone


class VectorMemory:
    def __init__(self, persist_dir: str = "data/memory"):
        self.persist_dir = persist_dir
        self.collection = None
        self.encoder = None
        self._initialize()

    def _initialize(self):
        os.makedirs(self.persist_dir, exist_ok=True)
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        except ImportError:
            self.encoder = None

        try:
            import chromadb
            client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = client.get_or_create_collection(
                name="farmer_memories",
                metadata={"hnsw:space": "cosine"},
            )
        except ImportError:
            self.collection = None

    def store_memory(self, user_id: int, memory_type: str, key: str,
                      content: str, metadata: Optional[Dict] = None,
                      importance: float = 0.5) -> str:
        memory_id = f"user_{user_id}_{memory_type}_{key}"
        timestamp = datetime.now(timezone.utc).isoformat()

        if self.collection and self.encoder:
            try:
                embedding = self.encoder.encode(content).tolist()
                doc_metadata = {
                    "user_id": str(user_id),
                    "memory_type": memory_type,
                    "key": key,
                    "importance": str(importance),
                    "timestamp": timestamp,
                }
                if metadata:
                    doc_metadata.update({k: str(v) for k, v in metadata.items()})

                self.collection.upsert(
                    ids=[memory_id],
                    embeddings=[embedding],
                    documents=[content],
                    metadatas=[doc_metadata],
                )
            except Exception as e:
                print(f"Vector store failed: {e}")

        self._store_fallback(user_id, memory_id, memory_type, key, content, metadata, importance, timestamp)
        return memory_id

    def search_memories(self, user_id: int, query: str, memory_type: Optional[str] = None, k: int = 10) -> List[Dict]:
        if self.collection and self.encoder:
            try:
                query_embedding = self.encoder.encode(query).tolist()
                filter_dict = {"user_id": str(user_id)}
                if memory_type:
                    filter_dict["memory_type"] = memory_type

                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=k,
                    where=filter_dict,
                )

                memories = []
                for i in range(len(results["documents"][0])):
                    memories.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "score": results["distances"][0][i] if results.get("distances") else 0.0,
                    })
                return memories
            except Exception as e:
                print(f"Vector search failed: {e}")

        return self._search_fallback(user_id, query, memory_type, k)

    def get_user_context(self, user_id: int) -> Dict[str, Any]:
        memories = self._get_all_fallback(user_id)
        disease_history = [m for m in memories if m.get("memory_type") == "disease"]
        preferences = [m for m in memories if m.get("memory_type") == "preference"]
        crops = [m for m in memories if m.get("memory_type") == "crop"]

        return {
            "disease_history": [
                {"disease": m.get("content", ""), "date": m.get("timestamp", "")}
                for m in disease_history[-10:]
            ],
            "preferences": {m.get("key", ""): m.get("content", "") for m in preferences},
            "crops_grown": [m.get("content", "") for m in crops],
            "total_memories": len(memories),
        }

    def delete_user_memories(self, user_id: int):
        if self.collection:
            try:
                self.collection.delete(where={"user_id": str(user_id)})
            except Exception:
                pass
        fallback_path = os.path.join(self.persist_dir, f"user_{user_id}_memories.json")
        if os.path.exists(fallback_path):
            os.remove(fallback_path)

    def _store_fallback(self, user_id: int, memory_id: str, memory_type: str, key: str,
                         content: str, metadata: Optional[Dict], importance: float, timestamp: str):
        fallback_path = os.path.join(self.persist_dir, f"user_{user_id}_memories.json")
        memories = []
        if os.path.exists(fallback_path):
            with open(fallback_path, "r") as f:
                memories = json.load(f)

        memories.append({
            "id": memory_id,
            "memory_type": memory_type,
            "key": key,
            "content": content,
            "metadata": metadata or {},
            "importance": importance,
            "timestamp": timestamp,
        })

        with open(fallback_path, "w") as f:
            json.dump(memories, f, indent=2, default=str)

    def _search_fallback(self, user_id: int, query: str, memory_type: Optional[str], k: int) -> List[Dict]:
        memories = self._get_all_fallback(user_id)
        if memory_type:
            memories = [m for m in memories if m.get("memory_type") == memory_type]

        query_lower = query.lower()
        scored = []
        for m in memories:
            content = m.get("content", "").lower()
            score = sum(1 for word in query_lower.split() if word in content)
            if score > 0:
                scored.append({**m, "score": score})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:k]

    def _get_all_fallback(self, user_id: int) -> List[Dict]:
        fallback_path = os.path.join(self.persist_dir, f"user_{user_id}_memories.json")
        if os.path.exists(fallback_path):
            with open(fallback_path, "r") as f:
                return json.load(f)
        return []
