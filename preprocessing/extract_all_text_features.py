import os
import torch
import pickle
from transformers import DistilBertTokenizer, DistilBertModel
from tqdm import tqdm

# Paths
TEXT_FOLDER = 'data/mini_dataset/segmented_transcripts'
OUTPUT_PATH = 'data/mini_dataset/mini_text_features.pkl'

# Load DistilBERT model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')
model.eval()

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

def extract_text_features(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512).to(device)

    # Get embeddings from DistilBERT
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()  # Mean pooling over tokens

    return embeddings

def main():
    text_feature_dict = {}

    print("Extracting text features from all transcripts...\n")

    for filename in tqdm(os.listdir(TEXT_FOLDER)):
        if filename.endswith('.txt'):
            clip_id = filename.replace('.txt', '')
            text_path = os.path.join(TEXT_FOLDER, filename)

            with open(text_path, 'r', encoding='utf-8') as f:
                transcript = f.read()

            features = extract_text_features(transcript)
            text_feature_dict[clip_id] = features

    # Save all extracted features
    with open(OUTPUT_PATH, 'wb') as f:
        pickle.dump(text_feature_dict, f)

    print(f"\n✅ Extracted text features for {len(text_feature_dict)} clips.")
    print(f"🔸 Saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
