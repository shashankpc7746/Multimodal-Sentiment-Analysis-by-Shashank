import os
import cv2
import torch
import pickle
import numpy as np
from tqdm import tqdm
from torchvision import models, transforms

# Paths
VIDEO_FOLDER = 'data/mini_dataset/segmented_video'
OUTPUT_PATH = 'data/mini_dataset/mini_video_features.pkl'

# Pretrained CNN model (ResNet18)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
resnet = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
resnet = torch.nn.Sequential(*list(resnet.children())[:-1])  # Remove final classifier
resnet.to(device)
resnet.eval()

# Preprocessing transform
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def extract_all_video_features(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_features = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            input_tensor = transform(frame).unsqueeze(0).to(device)

            with torch.no_grad():
                feature = resnet(input_tensor).squeeze().cpu().numpy()
                frame_features.append(feature)
        except Exception as e:
            print(f"Error in frame: {e}")
            continue

    cap.release()

    if frame_features:
        return np.mean(frame_features, axis=0)  # average across all frames
    else:
        return None

def main():
    feature_dict = {}

    print("Extracting CNN features from all segmented video clips...\n")

    for filename in tqdm(os.listdir(VIDEO_FOLDER)):
        if filename.endswith('.mp4'):
            clip_id = filename.replace('.mp4', '')
            video_path = os.path.join(VIDEO_FOLDER, filename)
            features = extract_all_video_features(video_path)
            if features is not None:
                feature_dict[clip_id] = features

    # Save all extracted features
    with open(OUTPUT_PATH, 'wb') as f:
        pickle.dump(feature_dict, f)

    print(f"\n✅ Extracted CNN features for {len(feature_dict)} video clips.")
    print(f"🔸 Saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
