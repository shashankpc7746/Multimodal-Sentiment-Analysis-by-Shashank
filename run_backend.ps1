# Backend Startup Script (uses py launcher - fixes venv python.exe stub issue)
$ProjectRoot = "d:\SHASHANK\Vs-code\Multimodal Sentiment Analysis by Shashank"
$VenvSitePackages = "$ProjectRoot\multimodal_env\Lib\site-packages"
$ApiDir = "$ProjectRoot\api"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Multimodal Sentiment Analysis Backend" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set PYTHONPATH to include venv site-packages
$env:PYTHONPATH = "$VenvSitePackages;$ApiDir;$ProjectRoot"

Write-Host "Loading models (this may take 10-15 seconds)..." -ForegroundColor Yellow
Write-Host ""

Set-Location $ApiDir
py -3.10 -m uvicorn main:app --reload --port 8000

Write-Host ""
Write-Host "Backend stopped." -ForegroundColor Red
Read-Host "Press Enter to exit"
