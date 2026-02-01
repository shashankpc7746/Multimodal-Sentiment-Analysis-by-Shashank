@echo off
cd /d "C:\Multimodal Sentiment Analysis by Shashank\api"
"C:\Multimodal Sentiment Analysis by Shashank\multimodal_env\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000
