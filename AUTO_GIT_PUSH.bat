@echo off
title Auto-Push Code to GitHub
color 0A
echo ========================================================
echo   Agentic AI Trader -- Automatic GitHub Sync
echo ========================================================
echo.

set GIT_PATH="C:\Program Files\Git\cmd\git.exe"

if not exist %GIT_PATH% (
    set GIT_PATH=git
)

echo [1/3] Staging modified and new files...
%GIT_PATH% add .

echo [2/3] Creating commit...
%GIT_PATH% commit -m "Auto-update code: %date% %time%"

echo [3/3] Pushing to GitHub (https://github.com/bheemesh7744/stock-market-prediction.git)...
%GIT_PATH% push origin main

echo.
echo ========================================================
echo   SUCCESS! GitHub, Vercel, and Render are updating!
echo ========================================================
echo.
pause
