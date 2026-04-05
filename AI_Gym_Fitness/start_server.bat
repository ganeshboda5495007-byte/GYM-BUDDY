@echo off
title AI Gym & Fitness Server
color 0A
echo ====================================
echo   AI Gym & Fitness Assistant
echo ====================================
echo.
cd /d "%~dp0"
echo Starting server...
echo.
python app.py
pause
