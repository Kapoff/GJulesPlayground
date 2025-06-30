@echo off

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"

REM Activate virtual environment
if exist "%SCRIPT_DIR%venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%SCRIPT_DIR%venv\Scripts\activate.bat"
) else (
    echo Virtual environment 'venv' not found. Please run setup first.
    exit /b 1
)

echo Starting Flask web server (for adding ingredients)...
REM Start Flask app in a new window minimized, as true backgrounding is tricky
start "Flask Server" /MIN python "%SCRIPT_DIR%app.py"
echo Flask app running. Access it at http://127.0.0.1:5000/
echo Note: The Flask server window will be minimized. Close it manually when done, or it will close when this main script window is closed.

echo Starting CLI application...
python "%SCRIPT_DIR%main_cli.py"

echo.
echo CLI application has finished.
echo Closing Flask server (if it was started by this script and is still running)...
REM Attempt to close the Flask server by title. This may not always work reliably.
taskkill /FI "WINDOWTITLE eq Flask Server*" /IM python.exe /F >nul 2>&1

REM Deactivate virtual environment
if defined VIRTUAL_ENV (
    echo Deactivating virtual environment...
    call "%SCRIPT_DIR%venv\Scripts\deactivate.bat"
)

echo Exiting.
pause
