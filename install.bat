@echo off
echo Case File Organizer - Installation Script
echo =======================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or later from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Display Python version
python --version
echo.

:: Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed!
    echo Please ensure pip is installed with Python.
    echo.
    pause
    exit /b 1
)

:: Ask user if they want to create a virtual environment
set /p create_venv="Do you want to create a virtual environment? (y/n): "
if /i "%create_venv%"=="y" (
    :: Create virtual environment if it doesn't exist
    if not exist "venv" (
        echo Creating virtual environment...
        python -m venv venv
        if errorlevel 1 (
            echo [ERROR] Failed to create virtual environment.
            pause
            exit /b 1
        )
    )
    
    :: Activate virtual environment
    echo Activating virtual environment...
    call venv\Scripts\activate
    if errorlevel 1 (
        echo [ERROR] Failed to activate virtual environment.
        pause
        exit /b 1
    )
)

:: Install/Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip, continuing with existing version...
)
echo.

:: Install required packages
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install required packages.
    pause
    exit /b 1
)

echo.
echo =======================================
echo Installation completed successfully!
echo.
echo To run the application:
echo 1. If using virtual environment, activate it with: venv\Scripts\activate
echo 2. Run the application with: python src/case_file_organizer.py
echo.
echo For building the executable:
echo 1. If using virtual environment, activate it with: venv\Scripts\activate
echo 2. Run the build script with: build.bat
echo =======================================
echo.

pause 