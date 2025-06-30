@echo off

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"
set "URL=http://127.0.0.1:5000/"

REM Activate virtual environment
if exist "%SCRIPT_DIR%venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%SCRIPT_DIR%venv\Scripts\activate.bat"
) else (
    echo Virtual environment 'venv' not found. Please run setup first.
    exit /b 1
)

echo Starting Flask web server...

REM Attempt to open the web browser first, then start server.
REM This way, if server start fails, user isn't left with just a browser window.
echo Attempting to open web browser to %URL%...
start "" "%URL%"

REM Give the browser a moment to launch, and server a head start if needed by browser.
timeout /t 2 /nobreak > nul

REM Run Flask app directly in this console. The script will wait here until Flask exits.
python "%SCRIPT_DIR%app.py"

REM When app.py (Flask server) is shut down (e.g., via the web UI button),
REM control will return here.

REM Deactivate virtual environment
if defined VIRTUAL_ENV (
    echo Flask server has shut down.
    echo Deactivating virtual environment...
    call "%SCRIPT_DIR%venv\Scripts\deactivate.bat"
)

echo Exiting.
exit /b 0
