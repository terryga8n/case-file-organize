@echo off
echo Building Case File Organizer...

:: Clean previous builds
echo Cleaning previous builds...
cd ..
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q release 2>nul
cd src

:: Install required packages
echo Installing required packages...
pip install pyinstaller pillow

:: Build the executable
echo Building executable...
pyinstaller --noconfirm --onefile --windowed --name "Case File Organizer" case_file_organizer.py

:: Create release package
echo Creating release package...
cd ..
mkdir release 2>nul
copy "dist\Case File Organizer.exe" "release\"
copy README.md release\
copy LICENSE release\

:: Create docs folder in release
mkdir release\docs
copy docs\* release\docs\

:: Create ZIP file
echo Creating ZIP file...
powershell Compress-Archive -Path "release\*" -DestinationPath "Case_File_Organizer_v1.0.0.zip" -Force

echo Build complete!
echo The executable is in the dist folder
echo The release package is in Case_File_Organizer_v1.0.0.zip
pause 