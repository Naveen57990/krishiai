import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
import json
import os


class CropRecommender:
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.crop_data = self._load_crop_data()
        self._load_model(model_path)

    def _load_crop_data(self) -> pd.DataFrame:
        data = [
            {"crop": "Rice", "N": 80, "P": 40, "K": 40, "temperature": 25, "humidity": 80, "ph": 6.5, "rainfall": 200, "soil_type": "clay"},
            {"crop": "Wheat", "N": 60, "P": 30, "K": 30, "temperature": 20, "humidity": 65, "ph": 6.8, "rainfall": 100, "soil_type": "loam"},
            {"crop": "Maize", "N": 80, "P": 40, "K": 20, "temperature": 25, "humidity": 70, "ph": 6.5, "rainfall": 100, "soil_type": "loam"},
            {"crop": "Sugarcane", "N": 100, "P": 60, "K": 40, "temperature": 28, "humidity": 75, "ph": 6.5, "rainfall": 200, "soil_type": "clay"},
            {"crop": "Cotton", "N": 60, "P": 30, "K": 30, "temperature": 30, "humidity": 60, "ph": 7.0, "rainfall": 100, "soil_type": "black"},
            {"crop": "Groundnut", "N": 20, "P": 40, "K": 30, "temperature": 27, "humidity": 65, "ph": 6.0, "rainfall": 80, "soil_type": "sandy"},
            {"crop": "Tomato", "N": 60, "P": 40, "K": 50, "temperature": 22, "humidity": 70, "ph": 6.5, "rainfall": 80, "soil_type": "loam"},
            {"crop": "Potato", "N": 80, "P": 50, "K": 60, "temperature": 18, "humidity": 75, "ph": 5.8, "rainfall": 70, "soil_type": "sandy"},
            {"crop": "Chilli", "N": 50, "P": 30, "K": 30, "temperature": 25, "humidity": 65, "ph": 6.5, "rainfall": 80, "soil_type": "loam"},
            {"crop": "Onion", "N": 60, "P": 40, "K": 40, "temperature": 22, "humidity": 65, "ph": 6.5, "rainfall": 70, "soil_type": "loam"},
            {"crop": "Soybean", "N": 30, "P": 50, "K": 40, "temperature": 25, "humidity": 70, "ph": 6.5, "rainfall": 90, "soil_type": "loam"},
            {"crop": "Pigeonpea", "N": 25, "P": 40, "K": 20, "temperature": 28, "humidity": 65, "ph": 6.5, "rainfall": 80, "soil_type": "loam"},
            {"crop": "Mungbean", "N": 20, "P": 30, "K": 20, "temperature": 27, "humidity": 70, "ph": 6.5, "rainfall": 75, "soil_type": "loam"},
            {"crop": "Jute", "N": 40, "P": 20, "K": 20, "temperature": 28, "humidity": 80, "ph": 6.5, "rainfall": 150, "soil_type": "clay"},
            {"crop": "Mustard", "N": 40, "P": 30, "K": 20, "temperature": 18, "humidity": 60, "ph": 6.5, "rainfall": 60, "soil_type": "loam"},
        ]
        return pd.DataFrame(data)

    def _load_model(self, model_path: Optional[str] = None):
        try:
            import joblib
            if model_path and os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print(f"Model loaded from {model_path}")
            else:
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.preprocessing import StandardScaler, LabelEncoder
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
                self.scaler = StandardScaler()
                self.label_encoder = LabelEncoder()
                print("Using sklearn model")
        except ImportError:
            print("scikit-learn not available, using rule-based recommender")
        except Exception as e:
            print(f"Model loading failed: {e}")

    def train(self, data_path: Optional[str] = None):
        if data_path and os.path.exists(data_path):
            df = pd.read_csv(data_path)
        else:
            df = self.crop_data.copy()

        if self.model is None:
            return

        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler, LabelEncoder

        features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        X = df[features]
        y = df["crop"]

        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model.fit(X_scaled, y_encoded)
        accuracy = self.model.score(X_scaled, y_encoded)
        print(f"Model trained with accuracy: {accuracy:.4f}")

        import joblib
        model_dir = os.path.join(os.path.dirname(__file__), "models")
        os.makedirs(model_dir, exist_ok=True)
        joblib.dump(self.model, os.path.join(model_dir, "crop_recommender.pkl"))
        joblib.dump(self.scaler, os.path.join(model_dir, "scaler.pkl"))
        joblib.dump(self.label_encoder, os.path.join(model_dir, "label_encoder.pkl"))

    def recommend(self, N: float, P: float, K: float, temperature: float,
                   humidity: float, ph: float, rainfall: float,
                   soil_type: Optional[str] = None, season: Optional[str] = None) -> List[Dict]:
        if self.model is not None and self.scaler is not None:
            try:
                features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
                features_scaled = self.scaler.transform(features)
                proba = self.model.predict_proba(features_scaled)[0]
                top_indices = np.argsort(proba)[::-1][:5]
                results = []
                for idx in top_indices:
                    crop_name = self.label_encoder.inverse_transform([idx])[0]
                    results.append({
                        "crop": crop_name,
                        "confidence": round(float(proba[idx]), 4),
                    })
                return results
            except Exception as e:
                print(f"ML prediction failed: {e}")

        return self._rule_based_recommend(N, P, K, temperature, humidity, ph, rainfall, soil_type, season)

    def _rule_based_recommend(self, N: float, P: float, K: float, temperature: float,
                               humidity: float, ph: float, rainfall: float,
                               soil_type: Optional[str] = None, season: Optional[str] = None) -> List[Dict]:
        scores = []
        for _, crop in self.crop_data.iterrows():
            score = 0.0
            count = 0

            if abs(temperature - crop["temperature"]) <= 5:
                score += 1
            count += 1

            if abs(humidity - crop["humidity"]) <= 15:
                score += 1
            count += 1

            if abs(ph - crop["ph"]) <= 0.8:
                score += 1
            count += 1

            if abs(rainfall - crop["rainfall"]) <= 70:
                score += 1
            count += 1

            if soil_type and crop.get("soil_type", "").lower() == soil_type.lower():
                score += 1
            count += 1 if soil_type else 0

            if season:
                season_map = {"kharif": ["Rice", "Maize", "Sugarcane", "Cotton", "Groundnut", "Chilli", "Soybean", "Pigeonpea", "Jute"],
                              "rabi": ["Wheat", "Potato", "Onion", "Mustard", "Tomato"],
                              "summer": ["Mungbean", "Groundnut"]}
                for s, crops in season_map.items():
                    if season.lower() == s and crop["crop"] in crops:
                        score += 1
                        count += 1

            final_score = score / max(count, 1)
            scores.append({"crop": crop["crop"], "confidence": round(final_score, 4)})

        scores.sort(key=lambda x: x["confidence"], reverse=True)
        return scores[:5]

    def predict_single(self, features: Dict) -> List[Dict]:
        return self.recommend(
            N=features.get("N", 50),
            P=features.get("P", 30),
            K=features.get("K", 30),
            temperature=features.get("temperature", 25),
            humidity=features.get("humidity", 65),
            ph=features.get("ph", 6.5),
            rainfall=features.get("rainfall", 100),
            soil_type=features.get("soil_type"),
            season=features.get("season"),
        )
