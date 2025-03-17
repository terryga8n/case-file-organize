@echo off
echo Running tests for Case File Organizer...

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

:: Run unit tests
echo Running unit tests...
python -m unittest discover tests/unit -v

:: Run integration tests
echo Running integration tests...
python -m unittest discover tests/integration -v

echo Tests complete!
pause 