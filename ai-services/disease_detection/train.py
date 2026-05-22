import os
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image
import numpy as np
from typing import Tuple


class PlantVillageDataset(Dataset):
    def __init__(self, data_dir: str, transform=None):
        self.data_dir = data_dir
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.classes = sorted(os.listdir(data_dir))
        self.class_to_idx = {cls: i for i, cls in enumerate(self.classes)}
        self.images = []
        self.labels = []

        for cls in self.classes:
            cls_dir = os.path.join(data_dir, cls)
            if not os.path.isdir(cls_dir):
                continue
            for img_name in os.listdir(cls_dir):
                if img_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    self.images.append(os.path.join(cls_dir, img_name))
                    self.labels.append(self.class_to_idx[cls])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert("RGB")
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label


def train_model(
    data_dir: str,
    model_dir: str,
    num_epochs: int = 50,
    batch_size: int = 32,
    learning_rate: float = 0.001,
    device: str = "cuda" if torch.cuda.is_available() else "cpu",
) -> Tuple[float, float]:
    os.makedirs(model_dir, exist_ok=True)

    dataset = PlantVillageDataset(os.path.join(data_dir, "train"))
    val_dataset = PlantVillageDataset(os.path.join(data_dir, "val"))

    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    model = models.efficientnet_b0(weights="IMAGENET1K_V1")
    num_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(num_features, len(dataset.classes))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=5)

    best_acc = 0.0
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        model.eval()
        correct = 0
        total = 0
        val_loss = 0.0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        accuracy = correct / total
        print(f"Epoch {epoch+1}/{num_epochs}: Train Loss: {running_loss/len(train_loader):.4f}, "
              f"Val Loss: {val_loss/len(val_loader):.4f}, Val Acc: {accuracy:.4f}")

        scheduler.step(val_loss / len(val_loader))

        if accuracy > best_acc:
            best_acc = accuracy
            torch.save(model.state_dict(), os.path.join(model_dir, "disease_model.pt"))
            print(f"Model saved with accuracy: {accuracy:.4f}")

    with open(os.path.join(model_dir, "classes.txt"), "w") as f:
        for cls in dataset.classes:
            f.write(f"{cls}\n")

    return best_acc, val_loss / len(val_loader)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Plant Disease Detection Model")
    parser.add_argument("--data-dir", type=str, required=True, help="Path to PlantVillage dataset")
    parser.add_argument("--model-dir", type=str, default="models", help="Path to save model")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    args = parser.parse_args()

    accuracy, loss = train_model(args.data_dir, args.model_dir, args.epochs, args.batch_size, args.lr)
    print(f"Training completed. Best accuracy: {accuracy:.4f}, Final loss: {loss:.4f}")
