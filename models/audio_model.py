import torch
import torch.nn as nn
import pickle

class AudioSentimentModel(nn.Module):
    def __init__(self, input_dim=40, hidden_dim=128, output_dim=3):
        super(AudioSentimentModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.fc(x)

def load_audio_features(path="data/audio_features.pkl"):
    with open(path, "rb") as f:
        features = pickle.load(f)
    first_file = list(features.keys())[0]
    feature_array = features[first_file]  # This is a NumPy array
    return torch.tensor(feature_array, dtype=torch.float32)  # Now valid

if __name__ == "__main__":
    features = load_audio_features().unsqueeze(0)  # Add batch dim: (1, 40)

    model = AudioSentimentModel()
    model.eval()

    with torch.no_grad():
        output = model(features)
        predicted = torch.argmax(output, dim=1).item()

    labels = ["Negative", "Neutral", "Positive"]
    print(f"Predicted Sentiment from Audio: {labels[predicted]}")
