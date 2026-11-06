@echo off
cd /d "%~dp0"
python khoi_phuc.py
if errorlevel 1 pause
