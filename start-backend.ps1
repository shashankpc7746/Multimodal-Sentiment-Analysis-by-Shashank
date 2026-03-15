# Backend API Server Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Multimodal Sentiment Analysis Backend" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "d:\SHASHANK\Vs-code\Multimodal Sentiment Analysis by Shashank\api"

Write-Host "Loading models (this may take 10-15 seconds)..." -ForegroundColor Yellow
Write-Host ""

& "d:/SHASHANK/Vs-code/Multimodal Sentiment Analysis by Shashank/multimodal_env/Scripts/python.exe" -m uvicorn main:app --reload --port 8000

Write-Host ""
Write-Host "Backend stopped." -ForegroundColor Red
Read-Host "Press Enter to exit"
