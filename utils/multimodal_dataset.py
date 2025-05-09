import os
import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset
from transformers import DistilBertTokenizer

class MultimodalDataset(Dataset):
    def __init__(self, csv_path, audio_dir, video_dir, tokenizer_name='distilbert-base-uncased', max_len=128):
        self.data = pd.read_csv(csv_path)
        self.audio_dir = audio_dir
        self.video_dir = video_dir
        self.tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_name)
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        clip_id = f"{row['video_id']}_{row['clip_id']}"
        label = row['annotation']
        label_map = {"Negative": 0, "Neutral": 1, "Positive": 2}
        label = label_map[label]

        # Text tokenization
        text = row['text']
        encoded = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        # Audio (MFCC)
        audio_path = os.path.join(self.audio_dir, f"{clip_id}.npy")
        audio_features = np.load(audio_path)  # shape: (n_mfcc, time)
        audio_tensor = torch.tensor(audio_features, dtype=torch.float32)

        # Video (pre-extracted frame features)
        video_path = os.path.join(self.video_dir, f"{clip_id}.npy")
        video_features = np.load(video_path)  # shape: (n_frames, feature_dim)
        video_tensor = torch.tensor(video_features, dtype=torch.float32)

        return {
            'input_ids': encoded['input_ids'].squeeze(0),
            'attention_mask': encoded['attention_mask'].squeeze(0),
            'audio': audio_tensor,
            'video': video_tensor,
            'label': torch.tensor(label, dtype=torch.long)
        }
