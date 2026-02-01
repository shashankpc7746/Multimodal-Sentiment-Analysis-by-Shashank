"""
FastAPI backend for Multimodal Sentiment Analysis
Exposes REST API endpoints for the React frontend
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
api_dir = Path(__file__).parent
project_root = api_dir.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import numpy as np
import pickle
from tensorflow.keras.models import load_model
import tensorflow as tf

# Import preprocessing utilities
from preprocessing.extract_all_video_features import extract_all_video_features
from preprocessing.extract_audio import extract_audio
from preprocessing.extract_all_audio_features import extract_mfcc_features
from preprocessing.transcribe_audio import transcribe_audio
from preprocessing.extract_all_text_features import extract_text_features

app = FastAPI(
    title="Multimodal Sentiment Analysis API",
    description="API for analyzing sentiment from video, audio, and text",
    version="1.0.0"
)

# Configure CORS to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models and scalers at startup
MODEL_DIR = project_root / "models"
model = None
scaler_v = None
scaler_a = None
scaler_t = None
le = None

@app.on_event("startup")
async def load_models():
    """Load ML models and preprocessing objects"""
    global model, scaler_v, scaler_a, scaler_t, le
    
    try:
        model = load_model(str(MODEL_DIR / "final_multimodal_logits_model.h5"))
        
        with open(MODEL_DIR / "scaler_video.pkl", "rb") as f:
            scaler_v = pickle.load(f)
        
        with open(MODEL_DIR / "scaler_audio.pkl", "rb") as f:
            scaler_a = pickle.load(f)
        
        with open(MODEL_DIR / "scaler_text.pkl", "rb") as f:
            scaler_t = pickle.load(f)
        
        with open(MODEL_DIR / "label_encoder.pkl", "rb") as f:
            le = pickle.load(f)
        
        print("✅ Models loaded successfully")
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Multimodal Sentiment Analysis API",
        "version": "1.0.0"
    }

@app.post("/api/analyze")
async def analyze_video(file: UploadFile = File(...)):
    """
    Analyze sentiment from uploaded video/audio file
    
    Returns:
        - sentiment: Positive/Negative/Neutral
        - confidence: Overall confidence score
        - transcript: Extracted speech text
        - breakdown: Individual modality scores
    """
    
    if not model or not scaler_v or not scaler_a or not scaler_t or not le:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    # Validate file type
    allowed_extensions = ['.mp4', '.avi', '.mov', '.wav', '.mp3', '.m4a']
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    vid_path = None
    audio_wav_path = None
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            vid_path = tmp_file.name
            content = await file.read()
            tmp_file.write(content)
        
        # Step 1: Extract video features
        video_feat_raw = extract_all_video_features(vid_path)
        if video_feat_raw is None:
            raise HTTPException(status_code=500, detail="Could not extract video features")
        video_feat_scaled = scaler_v.transform(video_feat_raw.reshape(1, -1))[0]
        
        # Step 2: Extract audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_file:
            audio_wav_path = tmp_audio_file.name
        
        if not extract_audio(vid_path, audio_wav_path):
            raise HTTPException(status_code=500, detail="Could not extract audio from video")
        
        # Step 3: Transcribe audio
        transcript = transcribe_audio(audio_wav_path)
        
        # Step 4: Extract audio MFCC features
        mfcc_vec_raw = extract_mfcc_features(audio_wav_path)
        if mfcc_vec_raw is None:
            raise HTTPException(status_code=500, detail="Could not extract audio features")
        mfcc_vec_scaled = scaler_a.transform(mfcc_vec_raw.reshape(1, -1))[0]
        
        # Step 5: Extract text features
        text_feat_scaled = np.zeros(768)
        if transcript:
            text_feat_raw = extract_text_features(transcript)
            if text_feat_raw is not None:
                text_feat_scaled = scaler_t.transform(text_feat_raw.reshape(1, -1))[0]
        
        # Step 6: Run prediction
        X_vid = np.expand_dims(video_feat_scaled, 0)
        X_aud = np.expand_dims(mfcc_vec_scaled, 0)
        X_txt = np.expand_dims(text_feat_scaled, 0)
        
        preds = model.predict([X_aud, X_vid, X_txt])
        idx = np.argmax(preds, axis=1)[0]
        sentiment = le.inverse_transform([idx])[0]
        
        # Get probabilities for each class
        probabilities = tf.nn.softmax(preds[0]).numpy()
        prob_dict = {label: float(prob) for label, prob in zip(le.classes_, probabilities)}
        
        # Calculate confidence (max probability)
        confidence = float(np.max(probabilities))
        
        # Calculate individual modality contributions (simplified)
        # This is a rough estimation - real attribution would need attention weights
        video_score = float(video_feat_scaled.mean())
        audio_score = float(mfcc_vec_scaled.mean())
        text_score = float(text_feat_scaled.mean())
        
        # Normalize scores to 0-1 range for display
        total = abs(video_score) + abs(audio_score) + abs(text_score) + 1e-6
        video_contrib = abs(video_score) / total
        audio_contrib = abs(audio_score) / total
        text_contrib = abs(text_score) / total
        
        return JSONResponse({
            "success": True,
            "sentiment": sentiment,
            "confidence": confidence,
            "transcript": transcript or "No speech detected",
            "probabilities": prob_dict,
            "breakdown": {
                "video": float(video_contrib),
                "audio": float(audio_contrib),
                "text": float(text_contrib)
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    finally:
        # Cleanup temporary files
        if vid_path and os.path.exists(vid_path):
            try:
                os.remove(vid_path)
            except:
                pass
        if audio_wav_path and os.path.exists(audio_wav_path):
            try:
                os.remove(audio_wav_path)
            except:
                pass

@app.post("/api/analyze-text")
async def analyze_text(text: str):
    """
    Analyze sentiment from text input only
    """
    
    if not model or not scaler_t or not le:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # Extract text features
        text_feat_raw = extract_text_features(text)
        if text_feat_raw is None:
            raise HTTPException(status_code=500, detail="Could not extract text features")
        
        text_feat_scaled = scaler_t.transform(text_feat_raw.reshape(1, -1))[0]
        
        # Use zeros for video and audio
        video_feat_scaled = np.zeros(scaler_v.n_features_in_)
        mfcc_vec_scaled = np.zeros(scaler_a.n_features_in_)
        
        # Run prediction
        X_vid = np.expand_dims(video_feat_scaled, 0)
        X_aud = np.expand_dims(mfcc_vec_scaled, 0)
        X_txt = np.expand_dims(text_feat_scaled, 0)
        
        preds = model.predict([X_aud, X_vid, X_txt])
        idx = np.argmax(preds, axis=1)[0]
        sentiment = le.inverse_transform([idx])[0]
        
        probabilities = tf.nn.softmax(preds[0]).numpy()
        prob_dict = {label: float(prob) for label, prob in zip(le.classes_, probabilities)}
        confidence = float(np.max(probabilities))
        
        return JSONResponse({
            "success": True,
            "sentiment": sentiment,
            "confidence": confidence,
            "probabilities": prob_dict,
            "breakdown": {
                "video": 0.0,
                "audio": 0.0,
                "text": 1.0
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
