@echo off
REM Plant Disease Classification System - Quick Start Script for Windows

echo.
echo ========================================
echo Plant Disease Classification System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.13+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo What would you like to do?
echo.
echo 1. Train the model (required on first run)
echo 2. Run the Flask application
echo 3. Exit
echo.

set /p choice="Enter your choice (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo Starting model training...
    echo This may take several hours on first run.
    echo.
    python train_model.py
    if errorlevel 1 (
        echo ERROR: Model training failed
        pause
        exit /b 1
    )
    echo.
    echo Training complete!
    pause
    goto menu
) else if "%choice%"=="2" (
    echo.
    echo Checking if model exists...
    if not exist "models\plant_disease_model.h5" (
        echo ERROR: Model not found!
        echo Please train the model first by running this script and selecting option 1.
        pause
        exit /b 1
    )
    echo.
    echo Starting Flask application...
    echo.
    echo Open your browser and go to: http://localhost:5000
    echo.
    echo Press CTRL+C to stop the application.
    echo.
    python app.py
) else if "%choice%"=="3" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice!
    pause
    goto menu
)

:menu
choice /C 123 /M "Enter your choice (1/2/3): "
goto choice_%errorlevel%

:choice_1
python train_model.py
pause
goto menu

:choice_2
if not exist "models\plant_disease_model.h5" (
    echo ERROR: Model not found! Please train first.
    pause
    goto menu
)
python app.py
goto menu

:choice_3
exit /b 0

:error
echo An error occurred!
pause
exit /b 1
