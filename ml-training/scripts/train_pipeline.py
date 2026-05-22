import argparse
import subprocess
import sys
import os


def train_disease_model(data_dir: str, model_dir: str, epochs: int = 50, batch_size: int = 32):
    print("=" * 60)
    print("Training Disease Detection Model")
    print("=" * 60)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from ai_services.disease_detection.train import train_model
    accuracy, loss = train_model(data_dir, model_dir, epochs, batch_size)
    print(f"Disease model - Accuracy: {accuracy:.4f}, Loss: {loss:.4f}")
    return accuracy


def train_crop_recommender(data_path: str = None):
    print("\n" + "=" * 60)
    print("Training Crop Recommendation Model")
    print("=" * 60)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from ai_services.recommendation.crop_recommender import CropRecommender
    recommender = CropRecommender()
    recommender.train(data_path)
    print("Crop recommender trained")


def train_yield_predictor(data_path: str = None):
    print("\n" + "=" * 60)
    print("Training Yield Prediction Model")
    print("=" * 60)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from ai_services.yield_prediction.predictor import YieldPredictor
    predictor = YieldPredictor()
    predictor.train(data_path)
    print("Yield predictor trained")


def run_all_training(data_dir: str = None, model_dir: str = "models", epochs: int = 50):
    if data_dir and os.path.exists(data_dir):
        train_disease_model(data_dir, model_dir, epochs)
    train_crop_recommender()
    train_yield_predictor()
    print("\n" + "=" * 60)
    print("All models trained successfully!")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train all KrishiAI ML models")
    parser.add_argument("--data-dir", type=str, help="Path to PlantVillage dataset")
    parser.add_argument("--model-dir", type=str, default="models", help="Model output directory")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument("--disease-only", action="store_true", help="Train only disease model")
    parser.add_argument("--crop-only", action="store_true", help="Train only crop recommender")
    parser.add_argument("--yield-only", action="store_true", help="Train only yield predictor")
    args = parser.parse_args()

    if args.disease_only:
        train_disease_model(args.data_dir, args.model_dir, args.epochs)
    elif args.crop_only:
        train_crop_recommender()
    elif args.yield_only:
        train_yield_predictor()
    else:
        run_all_training(args.data_dir, args.model_dir, args.epochs)
