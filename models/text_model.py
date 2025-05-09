import torch
import torch.nn as nn
from transformers import DistilBertModel, DistilBertTokenizer
import os

# Define the model
class TextSentimentClassifier(nn.Module):
    def __init__(self, output_dim=128):
        super(TextSentimentClassifier, self).__init__()
        self.bert = DistilBertModel.from_pretrained("distilbert-base-uncased")
        self.fc = nn.Sequential(
            nn.Linear(self.bert.config.hidden_size, output_dim),
            nn.ReLU()
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_token = outputs.last_hidden_state[:, 0, :]  # (B, 768)
        return self.fc(cls_token)                       # (B, output_dim)


# Run inference using the preprocessed transcript
if __name__ == "__main__":
    # Load tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = TextSentimentClassifier()
    model.eval()

    # Path to preprocessed transcript
    transcript_path = "data/transcripts/sample_preprocessed_transcript.txt"

    # Read transcript
    if not os.path.exists(transcript_path):
        raise FileNotFoundError(f"Transcript not found at {transcript_path}")

    with open(transcript_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    # Tokenize
    encoding = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=64)

    # Inference
    with torch.no_grad():
        logits = model(input_ids=encoding["input_ids"], attention_mask=encoding["attention_mask"])
        predicted_class = torch.argmax(logits, dim=1).item()

    sentiment_labels = {0: "Negative", 1: "Neutral", 2: "Positive"}
    print(f"Predicted Sentiment from Text: {sentiment_labels[predicted_class]}")
