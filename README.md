# Multimodal Sentiment Analysis — TriSenti AI

## 🎬 Project Overview

This project implements a **Multimodal Sentiment Classifier** that analyzes video clips to predict sentiment as **Positive**, **Negative**, or **Neutral**. It fuses three modalities:

- **Video:** Visual features extracted from video frames using ResNet18.
- **Audio:** Acoustic features (MFCCs) extracted from the audio track.
- **Text:** Semantic features from transcribed speech using DistilBERT.

The project is served through a **React + TypeScript frontend (TriSenti AI)** connected to a **FastAPI Python backend**.

---

## ✨ Features

- Processes video, audio, and text modalities for sentiment analysis.
- Uses ResNet18 (video), MFCCs (audio), and DistilBERT (text embeddings).
- Early fusion mechanism to combine multimodal features.
- Trained on a subset of the CMU-MOSI mini dataset (76.25% accuracy).
- Modern **React/TypeScript** frontend with real-time analysis UI.
- **FastAPI** REST backend exposing `/api/analyze` and `/api/analyze-text` endpoints.

---

## 📂 Project Structure

```
├── api/
│   ├── main.py                         # FastAPI backend server
│   └── requirements.txt                # Backend-specific deps
├── frontend/                           # React + TypeScript (Vite) UI
│   ├── src/
│   └── package.json
├── preprocessing/
│   ├── extract_audio.py                # Extracts audio from video
│   ├── extract_all_audio_features.py   # MFCC feature extraction
│   ├── extract_all_video_features.py   # ResNet18 video features
│   ├── extract_all_text_features.py    # DistilBERT text embeddings
│   └── transcribe_audio.py             # Speech-to-text transcription
├── models/
│   ├── final_multimodal_logits_model.h5 # Trained fusion model
│   ├── multimodal_model.py             # Model definition & training script
│   ├── label_encoder.pkl
│   ├── scaler_audio.pkl
│   ├── scaler_text.pkl
│   └── scaler_video.pkl
├── training/
│   └── evaluate_model.py
├── data/
│   ├── mini_dataset/                   # Raw segmented clips
│   └── processed_dataset.csv
├── requirements.txt                    # Full Python dependencies
├── run_backend.ps1                     # ✅ Recommended backend start script
├── START_BACKEND.bat                   # Windows BAT alternative
└── START_FRONTEND.bat                  # Frontend start script
```

---

## 🚀 Running the Project

### Prerequisites

- Python 3.10
- Node.js (v18+)
- **FFmpeg** installed and on PATH
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html), add `bin/` to PATH
  - Linux: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`

### Installation

**1. Create and activate the virtual environment:**
```powershell
python -m venv multimodal_env
multimodal_env\Scripts\activate
```

**2. Install Python dependencies:**
```bash
pip install -r requirements.txt
```

**3. Install frontend dependencies:**
```bash
cd frontend
npm install
```

---

### ▶️ Start the Backend (Port 8000)

Open a terminal and run:

```powershell
cd "d:\SHASHANK\Vs-code\Multimodal Sentiment Analysis by Shashank\api"
$env:PYTHONPATH = "d:\SHASHANK\Vs-code\Multimodal Sentiment Analysis by Shashank\multimodal_env\Lib\site-packages;d:\SHASHANK\Vs-code\Multimodal Sentiment Analysis by Shashank"
py -3.10 -m uvicorn main:app --reload --port 8000
```

Or simply run the provided script:
```powershell
.\run_backend.ps1
```

You should see:
```
✅ Models loaded successfully
INFO: Uvicorn running on http://127.0.0.1:8000
```

---

### ▶️ Start the Frontend (Port 3000)

Open a **separate terminal**:

```bash
cd frontend
npm run dev
```

Then open **http://localhost:3000** in your browser.

- API Docs: http://localhost:8000/docs

---

## 📡 API Endpoints

### `POST /api/analyze`
Analyzes a video or audio file.

**Request:** `multipart/form-data` with a video/audio file  
**Response:**
```json
{
  "success": true,
  "sentiment": "Positive",
  "confidence": 0.89,
  "transcript": "Hello everyone! I'm excited to share...",
  "probabilities": { "Positive": 0.89, "Negative": 0.05, "Neutral": 0.06 },
  "breakdown": { "video": 0.35, "audio": 0.38, "text": 0.27 }
}
```

### `POST /api/analyze-text`
Analyzes raw text input (text-only mode).

---

## 📈 Model Results

Trained on 400 clips from the CMU-MOSI mini dataset:

| Metric | Value |
|---|---|
| Test Accuracy | **76.25%** |
| Positive F1 | 0.83 |
| Negative F1 | 0.71 |
| Neutral F1 | 0.44 |

---

## 🐛 Troubleshooting

- **Backend won't start?** — Check that all `.pkl` and `.h5` files exist in `models/`
- **Frontend can't connect?** — Ensure backend is on port `8000`; check browser console for CORS errors
- **Transcription failing?** — Requires internet connection (Google Speech Recognition API)
