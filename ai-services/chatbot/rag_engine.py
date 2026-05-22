import os
from typing import List, Optional, Dict
import json


class RAGEngine:
    def __init__(self, persist_dir: str = "data/chroma"):
        self.persist_dir = persist_dir
        self.collection = None
        self.embeddings_model = None
        self._initialize()

    def _initialize(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.embeddings_model = SentenceTransformer("all-MiniLM-L6-v2")
            print("SentenceTransformer loaded successfully")
        except ImportError:
            print("SentenceTransformer not available")
            self.embeddings_model = None

        try:
            import chromadb
            os.makedirs(self.persist_dir, exist_ok=True)
            client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = client.get_or_create_collection(
                name="krishiai_knowledge",
                metadata={"hnsw:space": "cosine"},
            )
            print("ChromaDB initialized")
        except ImportError:
            print("ChromaDB not available")
            self.collection = None

    def add_documents(self, documents: List[Dict[str, str]]):
        if not self.collection or not self.embeddings_model:
            print("Embeddings not available, storing raw documents")
            self._store_raw(documents)
            return

        texts = [doc["text"] for doc in documents]
        metadatas = [{"source": doc.get("source", ""), "title": doc.get("title", "")} for doc in documents]
        ids = [doc.get("id", str(hash(doc["text"]))) for doc in documents]

        embeddings = self.embeddings_model.encode(texts).tolist()
        self.collection.add(embeddings=embeddings, documents=texts, metadatas=metadatas, ids=ids)

    def search(self, query: str, k: int = 5) -> List[Dict]:
        if self.collection and self.embeddings_model:
            try:
                query_embedding = self.embeddings_model.encode(query).tolist()
                results = self.collection.query(query_embeddings=[query_embedding], n_results=k)
                documents = []
                for i in range(len(results["documents"][0])):
                    documents.append({
                        "text": results["documents"][0][i],
                        "source": results["metadatas"][0][i].get("source", ""),
                        "score": results["distances"][0][i] if results.get("distances") else 0.0,
                    })
                return documents
            except Exception as e:
                print(f"Search error: {e}")

        return self._search_raw(query, k)

    def _store_raw(self, documents: List[Dict]):
        raw_path = os.path.join(self.persist_dir, "raw_knowledge.json")
        existing = []
        if os.path.exists(raw_path):
            with open(raw_path, "r") as f:
                existing = json.load(f)
        existing.extend(documents)
        with open(raw_path, "w") as f:
            json.dump(existing, f, indent=2)

    def _search_raw(self, query: str, k: int = 5) -> List[Dict]:
        raw_path = os.path.join(self.persist_dir, "raw_knowledge.json")
        if not os.path.exists(raw_path):
            return self._get_default_knowledge(query, k)

        with open(raw_path, "r") as f:
            documents = json.load(f)

        query_lower = query.lower()
        scored = []
        for doc in documents:
            text_lower = doc.get("text", "").lower()
            score = sum(1 for word in query_lower.split() if word in text_lower)
            if score > 0:
                scored.append({"text": doc["text"], "source": doc.get("source", ""), "score": score})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:k] if scored else self._get_default_knowledge(query, k)

    def _get_default_knowledge(self, query: str, k: int = 3) -> List[Dict]:
        knowledge = [
            {"text": "Rice requires 1000-2500mm rainfall and temperature of 20-35°C. Best grown in clay loam soil with pH 5.0-7.5.", "source": "crop_guide"},
            {"text": "Wheat requires 500-1500mm rainfall and temperature of 10-30°C. Best grown in loam soil with pH 6.0-7.5.", "source": "crop_guide"},
            {"text": "Tomato Early Blight: Apply chlorothalonil 2g/L or mancozeb 2g/L every 7-10 days. Remove infected leaves.", "source": "disease_guide"},
            {"text": "Rice Blast: Apply tricyclazole 75% WP at 0.6g/L or carbendazim 50% WP at 1g/L. Use resistant varieties.", "source": "disease_guide"},
            {"text": "For irrigation, drip irrigation saves 30-50% water compared to flood irrigation. Best for vegetables.", "source": "farming_tips"},
            {"text": "Neem oil 3% is an effective organic pesticide for most crop pests. Apply every 7-10 days.", "source": "organic_farming"},
            {"text": "Soil testing should be done every 2-3 years. Optimal pH for most crops is 6.0-7.0.", "source": "soil_management"},
        ]
        return knowledge[:k]

    def add_farming_knowledge(self):
        documents = [
            {"id": "crop_rice", "text": "Rice (Oryza sativa) is a kharif crop requiring 1000-2500mm annual rainfall. Optimal temperature range is 20-35°C. Best suited for clay loam soils with pH 5.0-7.5. Growing period is 120-150 days. High water requirement.", "source": "crop_database", "title": "Rice Cultivation Guide"},
            {"id": "crop_wheat", "text": "Wheat (Triticum aestivum) is a rabi crop requiring 500-1500mm rainfall. Optimal temperature 10-30°C. Requires well-drained loam soil with pH 6.0-7.5. Growing period 140-160 days.", "source": "crop_database", "title": "Wheat Cultivation Guide"},
            {"id": "crop_maize", "text": "Maize (Zea mays) is a kharif crop. Requires 600-1200mm rainfall. Temperature range 18-35°C. Grows best in loam soils pH 5.5-7.5. Growing period 90-110 days.", "source": "crop_database", "title": "Maize Cultivation Guide"},
            {"id": "disease_tomato_early_blight", "text": "Early Blight in tomato caused by Alternaria solani. Symptoms: dark spots with concentric rings on leaves. Treatment: Chlorothalonil 75% WP 2g/L or Mancozeb 75% WP 2g/L every 7-10 days. Organic: Neem oil 3% spray.", "source": "disease_database", "title": "Tomato Early Blight Management"},
            {"id": "disease_rice_blast", "text": "Rice Blast caused by Magnaporthe oryzae. Symptoms: diamond-shaped lesions on leaves, neck rot. Treatment: Tricyclazole 75% WP 0.6g/L. Prevention: Use resistant varieties, avoid excess nitrogen.", "source": "disease_database", "title": "Rice Blast Management"},
            {"id": "organic_farming", "text": "Organic farming uses natural inputs like compost, neem oil, and beneficial insects. Avoids synthetic pesticides and fertilizers. Promotes soil health and biodiversity. Use neem cake as fertilizer and neem oil 3% as pesticide.", "source": "farming_practices", "title": "Organic Farming Basics"},
            {"id": "irrigation_tips", "text": "Drip irrigation saves 30-50% water. Best for vegetables, fruits, and cash crops. Sprinkler irrigation suitable for cereals. Flood irrigation traditional but inefficient. Best time to irrigate is early morning or evening.", "source": "water_management", "title": "Irrigation Methods"},
            {"id": "soil_health", "text": "Test soil every 2-3 years. Optimal pH 6.0-7.0 for most crops. Add lime to increase pH, sulfur to decrease. Organic matter should be above 0.5%. Use green manuring to improve soil health.", "source": "soil_science", "title": "Soil Health Management"},
            {"id": "pest_management", "text": "Integrated Pest Management (IPM): Monitor crops weekly. Use pheromone traps. Introduce beneficial insects. Apply neem oil as preventive. Use chemical pesticides only when thresholds crossed.", "source": "pest_control", "title": "IPM Guide"},
            {"id": "fertilizer_guide", "text": "NPK 20:20:20 at 150kg/ha for most crops. Apply nitrogen in split doses. Phosphorus at planting. Potash at flowering. Use soil test based recommendations. Organic: Farmyard manure 10-15 tons/ha.", "source": "nutrition", "title": "Fertilizer Recommendations"},
        ]
        self.add_documents(documents)
        print(f"Added {len(documents)} farming knowledge documents")
        return documents
