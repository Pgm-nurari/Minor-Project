@echo off
title FinSight - Financial Event Management System
color 0A

echo.
echo ============================================================
echo        FinSight - Financial Event Management
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo.
    echo This appears to be your FIRST TIME running FinSight.
    echo.
    echo Please follow these steps:
    echo   1. Copy .env.example to .env
    echo   2. Edit .env and set your MySQL password
    echo   3. Make sure MySQL server is running
    echo   4. Run this script again
    echo.
    echo Quick setup command:
    echo   copy .env.example .env
    echo.
    echo See FIRST_TIME_SETUP.md for detailed instructions.
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Virtual environment not found. Creating...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
    echo.
)

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [INFO] Virtual environment activated
    echo.
)

REM Check if requirements are installed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
    echo [SUCCESS] Dependencies installed
    echo.
)

echo [INFO] Starting FinSight...
echo.
echo Visit: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

REM Run the application
python run.py

REM If there's an error, pause to show the message
if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start
    echo Check the error messages above
    pause
)
