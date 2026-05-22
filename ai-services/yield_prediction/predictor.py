import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple
import os
import json


class YieldPredictor:
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.base_yields = self._get_base_yields()
        self._load_model(model_path)

    def _get_base_yields(self) -> Dict[str, float]:
        return {
            "Rice": 4000, "Wheat": 3500, "Maize": 5000, "Sugarcane": 70000,
            "Cotton": 2500, "Groundnut": 2500, "Soybean": 2500, "Potato": 25000,
            "Tomato": 30000, "Onion": 25000, "Chilli": 15000, "Turmeric": 15000,
            "Banana": 35000, "Mango": 10000, "Coconut": 15000, "Orange": 20000,
            "Grapes": 15000, "Pomegranate": 12000, "Papaya": 40000,
        }

    def _load_model(self, model_path: Optional[str] = None):
        try:
            import joblib
            if model_path and os.path.exists(model_path):
                self.model = joblib.load(model_path)
                print(f"Yield model loaded from {model_path}")
            else:
                from sklearn.ensemble import GradientBoostingRegressor
                self.model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
                print("Using GradientBoostingRegressor")
        except ImportError:
            print("scikit-learn not available, using rule-based predictor")
        except Exception as e:
            print(f"Model loading failed: {e}")

    def train(self, data_path: Optional[str] = None):
        if not self.model:
            return

        np.random.seed(42)
        n_samples = 1000
        data = {
            "crop": np.random.choice(list(self.base_yields.keys()), n_samples),
            "area": np.random.uniform(0.5, 10, n_samples),
            "temperature": np.random.uniform(15, 35, n_samples),
            "rainfall": np.random.uniform(200, 2000, n_samples),
            "ph": np.random.uniform(5.0, 8.0, n_samples),
            "fertilizer_n": np.random.uniform(20, 120, n_samples),
            "fertilizer_p": np.random.uniform(10, 60, n_samples),
            "fertilizer_k": np.random.uniform(10, 60, n_samples),
        }

        df = pd.DataFrame(data)
        df["base_yield"] = df["crop"].map(self.base_yields)

        noise = np.random.normal(0, df["base_yield"].std() * 0.1, n_samples)
        temp_effect = -0.02 * (df["temperature"] - 25) ** 2
        rain_effect = -0.01 * (df["rainfall"] - 800) ** 2 / 1000
        ph_effect = -0.1 * (df["ph"] - 6.5) ** 2
        fert_effect = 0.001 * (df["fertilizer_n"] + df["fertilizer_p"] + df["fertilizer_k"])

        df["yield_kg"] = df["base_yield"] * df["area"] * (1 + temp_effect + rain_effect + ph_effect + fert_effect) + noise
        df["yield_kg"] = df["yield_kg"].clip(lower=0)

        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        df["crop_encoded"] = le.fit_transform(df["crop"])

        features = ["crop_encoded", "area", "temperature", "rainfall", "ph", "fertilizer_n", "fertilizer_p", "fertilizer_k"]
        X = df[features]
        y = df["yield_kg"]

        self.model.fit(X, y)
        r2 = self.model.score(X, y)
        print(f"Yield model trained with R²: {r2:.4f}")

        import joblib
        model_dir = os.path.join(os.path.dirname(__file__), "models")
        os.makedirs(model_dir, exist_ok=True)
        joblib.dump(self.model, os.path.join(model_dir, "yield_predictor.pkl"))

    def predict(self, crop_name: str, area_hectares: float,
                soil_type: Optional[str] = None, ph_level: Optional[float] = None,
                rainfall_mm: Optional[float] = None, temperature: Optional[float] = None,
                fertilizer_n: float = 60, fertilizer_p: float = 30, fertilizer_k: float = 30) -> Dict:

        if self.model is not None:
            try:
                from sklearn.preprocessing import LabelEncoder
                le = LabelEncoder()
                le.fit(list(self.base_yields.keys()))
                crop_encoded = le.transform([crop_name])[0]

                features = np.array([[
                    crop_encoded, area_hectares,
                    temperature or 25, rainfall_mm or 800, ph_level or 6.5,
                    fertilizer_n, fertilizer_p, fertilizer_k,
                ]])
                predicted = self.model.predict(features)[0]

                residuals = predicted * 0.1
                return {
                    "yield_kg": round(float(predicted), 2),
                    "ci_lower": round(float(predicted - 1.96 * residuals), 2),
                    "ci_upper": round(float(predicted + 1.96 * residuals), 2),
                }
            except Exception as e:
                print(f"ML prediction failed: {e}")

        return self._rule_based_predict(crop_name, area_hectares, temperature, rainfall_mm, ph_level)

    def _rule_based_predict(self, crop_name: str, area: float,
                             temperature: Optional[float], rainfall: Optional[float],
                             ph: Optional[float]) -> Dict:
        base = self.base_yields.get(crop_name, 5000)
        temp = temperature or 25
        rain = rainfall or 800
        ph_val = ph or 6.5

        temp_factor = 1 - 0.02 * (temp - 25) ** 2 / 100
        rain_factor = 1 - 0.01 * (rain - 800) ** 2 / 10000
        ph_factor = 1 - 0.1 * (ph_val - 6.5) ** 2 / 10

        predicted = base * area * max(0.3, temp_factor * rain_factor * ph_factor)
        residuals = predicted * 0.15

        return {
            "yield_kg": round(float(predicted), 2),
            "ci_lower": round(float(predicted - 1.96 * residuals), 2),
            "ci_upper": round(float(predicted + 1.96 * residuals), 2),
        }
