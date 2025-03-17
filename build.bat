@echo off
echo Building Case File Organizer...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or later.
    pause
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not installed. Please install pip.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

:: Check for icon file
if not exist "icon.ico" (
    echo Creating default icon...
    copy nul icon.ico
)

:: Clean previous builds
echo Cleaning previous builds...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

:: Build the executable
echo Building executable...
pyinstaller case_file_organizer.spec
if errorlevel 1 (
    echo Failed to build executable.
    pause
    exit /b 1
)

:: Verify executable was created
if not exist "dist\Case File Organizer.exe" (
    echo Executable was not created.
    pause
    exit /b 1
)

:: Create release package
echo Creating release package...
mkdir release 2>nul
xcopy /s /y dist\Case File Organizer\* release\
copy README.md release\
copy LICENSE release\
copy docs\user_guide.md release\

:: Create ZIP file
echo Creating ZIP file...
powershell Compress-Archive -Path release\* -DestinationPath Case_File_Organizer_v1.0.0.zip -Force
if errorlevel 1 (
    echo Failed to create ZIP file.
    pause
    exit /b 1
)

echo Build complete!
echo The executable is in the dist folder
echo The release package is in Case_File_Organizer_v1.0.0.zip
pause 