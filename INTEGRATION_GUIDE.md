# Multimodal Sentiment Analysis - Frontend/Backend Integration

## 🎉 Setup Complete!

Your frontend is now connected to a real Python backend that performs actual sentiment analysis.

## 🚀 How to Run

### 1. Start the Backend API (Port 8000)

Open a **new terminal** and run:

```powershell
cd "C:\Multimodal Sentiment Analysis by Shashank\api"
& "C:/Multimodal Sentiment Analysis by Shashank/multimodal_env/Scripts/python.exe" -m uvicorn main:app --reload --port 8000
```

You should see:
```
✅ Models loaded successfully
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2. Start the React Frontend (Port 3001 or 5173)

In another terminal (or use the existing one):

```powershell
cd "C:\Multimodal Sentiment Analysis by Shashank\frontend"
npm run dev
```

### 3. Open in Browser

- Frontend: http://localhost:3001 (or http://localhost:5173)
- Backend API Docs: http://localhost:8000/docs

## 🔧 What Changed

### Backend (NEW!)
- **Created**: `api/main.py` - FastAPI server with two endpoints:
  - `POST /api/analyze` - Analyzes video/audio files
  - `POST /api/analyze-text` - Analyzes text input
- **Features**:
  - Real video feature extraction
  - Real audio transcription (Google Speech Recognition)
  - Real sentiment prediction using your trained models
  - CORS enabled for React frontend

### Frontend (UPDATED!)
- **Modified**: `frontend/src/App.tsx`
  - Replaced mock `simulateAnalysis()` with real `analyzeWithBackend()`
  - Sends files to backend API via FormData
  - Displays real transcripts from actual speech recognition
  - Shows real sentiment predictions from ML models

## 🎯 What You'll Get Now

When you upload a video:
1. **Real transcription** from the actual audio (via Google Speech Recognition)
2. **Real sentiment** from your trained multimodal model
3. **Real confidence scores** based on model predictions
4. **Multimodal breakdown** showing video/audio/text contributions

## 📝 API Endpoints

### POST /api/analyze
Analyzes video/audio files

**Request**: `multipart/form-data` with file
**Response**:
```json
{
  "success": true,
  "sentiment": "Positive",
  "confidence": 0.89,
  "transcript": "Hello everyone! I'm excited to share...",
  "probabilities": {
    "Positive": 0.89,
    "Negative": 0.05,
    "Neutral": 0.06
  },
  "breakdown": {
    "video": 0.35,
    "audio": 0.38,
    "text": 0.27
  }
}
```

### POST /api/analyze-text
Analyzes text input

**Query Param**: `text=<your text here>`
**Response**: Same as above

## ✅ Dependencies Installed

```
fastapi==0.115.6
uvicorn[standard]==0.34.0
python-multipart==0.0.20
```

## 🐛 Troubleshooting

**Backend won't start?**
- Make sure port 8000 is free
- Check if all models exist in `models/` folder
- Verify virtual environment is activated

**Frontend can't connect?**
- Check backend is running on http://localhost:8000
- Check browser console for CORS errors
- Verify both servers are running

**Transcription not working?**
- Requires active internet connection (Google Speech Recognition API)
- Audio must have clear speech
- Video must have audio track

## 🎬 Ready to Test!

1. Upload a video with someone speaking
2. Watch real-time progress (4 steps)
3. See actual transcribed text
4. Get real sentiment analysis!

The lady in your video will now have her actual words transcribed! 🎤
