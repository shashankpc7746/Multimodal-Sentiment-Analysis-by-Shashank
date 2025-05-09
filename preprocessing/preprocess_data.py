import os
import pandas as pd
import pickle
import logging
from sklearn.model_selection import train_test_split

# === Logging Setup ===
log_path = os.path.join("training", "training_log.txt")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# === Paths ===
LABELS_PATH = os.path.join("data", "mini_dataset", "labels.csv")
OUTPUT_PATH = os.path.join("data", "mini_dataset", "processed_data.pkl")

# === Load Labels ===
try:
    df = pd.read_csv(LABELS_PATH)
    print(f"Initial Data Shape: {df.shape}")
    logging.info(f"Loaded labels from {LABELS_PATH} with shape {df.shape}")
except Exception as e:
    logging.error(f"Failed to load labels: {e}")
    raise

# === Drop NA if any (optional) ===
df.dropna(inplace=True)
print(f"After Dropping NA: {df.shape}")
logging.info(f"Data shape after dropping NA: {df.shape}")

# === Dummy Feature Extraction (Replace with real logic) ===
def load_dummy_features(df):
    df['text_feat'] = df['text'].apply(lambda x: [len(x)])  # dummy text feature
    df['audio_feat'] = df['label'].apply(lambda x: [x])     # dummy audio feature
    df['video_feat'] = df['label'].apply(lambda x: [x * 2])  # dummy video feature
    print("✅ Dummy features extracted.")
    logging.info("Applied dummy feature extraction.")
    return df

df = load_dummy_features(df)

# === Train/Val/Test Split ===
try:
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['annotation'])
    train_df, val_df = train_test_split(train_df, test_size=0.1, random_state=42, stratify=train_df['annotation'])

    print(f"Train size: {len(train_df)}, Val size: {len(val_df)}, Test size: {len(test_df)}")
    logging.info(f"Data split: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
except Exception as e:
    logging.error(f"Data splitting failed: {e}")
    raise

# === Save Preprocessed Data ===
def save_preprocessed_data(train, val, test, path):
    try:
        with open(path, "wb") as f:
            pickle.dump({'train': train, 'val': val, 'test': test}, f)
        print(f"✅ Saved train/val/test splits to {path}")
        logging.info(f"Saved preprocessed data to {path}")
    except Exception as e:
        logging.error(f"Failed to save preprocessed data: {e}")
        raise

save_preprocessed_data(train_df, val_df, test_df, OUTPUT_PATH)
