import torch
import torch.nn as nn
import pickle

class VideoSentimentModel(nn.Module):
    def __init__(self, input_dim=2048, hidden_dim=512, output_dim=3):
        super(VideoSentimentModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.fc(x)

def load_video_features(path="data/video_features.pkl"):
    with open(path, "rb") as f:
        features = pickle.load(f)
    return torch.tensor(features, dtype=torch.float32)

if __name__ == "__main__":
    # Load features
    features = load_video_features().unsqueeze(0)  # Add batch dim

    # Load model
    model = VideoSentimentModel()
    model.eval()

    # Predict
    with torch.no_grad():
        output = model(features)
        predicted = torch.argmax(output, dim=1).item()

    labels = ["Negative", "Neutral", "Positive"]
    print(f"Predicted Sentiment from Video: {labels[predicted]}")
