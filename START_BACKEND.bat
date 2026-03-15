@echo off
echo Starting Backend API Server...
echo.
cd /d "d:\SHASHANK\Vs-code\Multimodal Sentiment Analysis by Shashank\api"
call "d:\SHASHANK\Vs-code\Multimodal Sentiment Analysis by Shashank\multimodal_env\Scripts\activate.bat"
python -m uvicorn main:app --reload --port 8000
pause
