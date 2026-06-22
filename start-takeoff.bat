@echo off
cd /d "%~dp0"
echo Starting Steel Bar Takeoff...
echo.
python server.py
if errorlevel 1 (
  echo.
  echo Could not start. Make sure Python is installed and on your PATH.
  echo Download it from https://www.python.org/downloads/ if needed.
  pause
)
