@echo off
cd /d "d:\SHASHANK\Vs-code\Multimodal Sentiment Analysis by Shashank\api"
"d:\SHASHANK\Vs-code\Multimodal Sentiment Analysis by Shashank\multimodal_env\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000
