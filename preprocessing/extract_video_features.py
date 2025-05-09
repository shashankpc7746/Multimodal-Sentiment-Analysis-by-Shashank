import os
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
import numpy as np
import pickle

def extract_video_features(frame_dir, output_file="data/video_features.pkl"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load pretrained ResNet50 model with weights
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights=weights)
    model = torch.nn.Sequential(*list(model.children())[:-1])  # Remove classification layer
    model.eval().to(device)

    # Use official preprocessing from weights
    transform = weights.transforms()

    features = []

    for filename in sorted(os.listdir(frame_dir)):
        frame_path = os.path.join(frame_dir, filename)
        if filename.endswith(".jpg"):
            try:
                image = Image.open(frame_path).convert("RGB")
                image = transform(image).unsqueeze(0).to(device)

                with torch.no_grad():
                    feature = model(image).squeeze().cpu().numpy()
                features.append(feature)
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    features = np.array(features)
    avg_feature = np.mean(features, axis=0)

    # Save features
    with open(output_file, "wb") as f:
        pickle.dump(avg_feature, f)

    print(f"Video features saved to {output_file}")
    return avg_feature

# Example usage
if __name__ == "__main__":
    extract_video_features("data/processed_frames")