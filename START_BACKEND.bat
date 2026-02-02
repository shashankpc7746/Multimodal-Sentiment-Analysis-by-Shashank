@echo off
echo Starting Backend API Server...
echo.
cd /d "C:\Multimodal Sentiment Analysis by Shashank\api"
call "C:\Multimodal Sentiment Analysis by Shashank\multimodal_env\Scripts\activate.bat"
python -m uvicorn main:app --reload --port 8000
pause
