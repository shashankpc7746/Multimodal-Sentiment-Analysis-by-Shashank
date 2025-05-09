# utils/helper_functions.py

import torch
import numpy as np
from preprocessing.extract_frames import extract_frames
from preprocessing.extract_audio import extract_audio
from preprocessing.transcribe_audio import transcribe_audio
from models.cnn_video_model import CNNVideoModel
from models.audio_model import AudioFFNN
from models.text_model import TextBERTClassifier
from models.multimodal_model import MultimodalFusionModel
from utils.config import DEVICE # type: ignore
import torchvision.transforms as transforms
from sklearn.preprocessing import StandardScaler
from transformers import DistilBertTokenizer

@torch.no_grad()
def predict_sentiment(video_path):
    # ========== Step 1: Extract Modal Inputs ==========
    frames = extract_frames(video_path)              # list of PIL images
    audio_path = extract_audio(video_path)           # returns temp_audio.wav
    transcript = transcribe_audio(audio_path)        # returns string

    # ========== Step 2: Preprocess Inputs ==========
    # ----- Video -----
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor()
    ])
    frame_tensors = torch.stack([transform(frame) for frame in frames])
    video_input = frame_tensors.unsqueeze(0).to(DEVICE)   # shape: [1, N, 3, 128, 128]

    # ----- Audio -----
    from preprocessing.preprocess_data import extract_mfcc
    mfcc = extract_mfcc(audio_path)                  # shape: (n_mfcc,)
    scaler = StandardScaler()
    audio_input = torch.tensor(scaler.fit_transform(mfcc.reshape(1, -1)), dtype=torch.float32).to(DEVICE)

    # ----- Text -----
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    tokens = tokenizer(transcript, return_tensors="pt", padding=True, truncation=True).to(DEVICE)

    # ========== Step 3: Load Models ==========
    video_model = CNNVideoModel().to(DEVICE)
    video_model.load_state_dict(torch.load("models\cnn_video_model.py"))
    video_model.eval()

    audio_model = AudioFFNN().to(DEVICE)
    audio_model.load_state_dict(torch.load("models\audio_model.py"))
    audio_model.eval()

    text_model = TextBERTClassifier().to(DEVICE)
    text_model.load_state_dict(torch.load("models\text_model.py"))
    text_model.eval()

    fusion_model = MultimodalFusionModel().to(DEVICE)
    fusion_model.load_state_dict(torch.load("models\multimodal_model.py"))
    fusion_model.eval()

    # ========== Step 4: Get Embeddings ==========
    video_feat = video_model(video_input)
    audio_feat = audio_model(audio_input)
    text_feat = text_model(tokens)

    # ========== Step 5: Fuse & Predict ==========
    combined_logits = fusion_model(video_feat, audio_feat, text_feat)
    probs = torch.softmax(combined_logits, dim=1).squeeze()
    predicted_class = torch.argmax(probs).item()
    confidence = probs[predicted_class].item()

    return predicted_class, confidence, transcript
