@echo off
ECHO ======================================================
ECHO  AEGIS NETWORK LAUNCHER (WINDOWS)
ECHO ======================================================
ECHO.

:: --- CONTEXT CALIBRATION ---
:: Change directory to the parent folder (the project root)
cd /d "%~dp0\.."
ECHO Set working directory to: %cd%
ECHO.

ECHO This script will launch the 3 required components in separate windows.
ECHO Please ensure your virtual environment ('venv') is set up.
ECHO.

REM Activate virtual environment
CALL .\venv\Scripts\activate.bat

ECHO Launching Ledger Server on port 9000...
start "Aegis Ledger" cmd /k "uvicorn ledger_server:app --port 9000"

ECHO Waiting for 5 seconds for Ledger to initialize...
timeout /t 5 /nobreak > NUL

ECHO Launching Provider Node on port 8000...
start "Aegis Provider" cmd /k "uvicorn provider_node:app"

ECHO Waiting for 5 seconds for Provider to register...
timeout /t 5 /nobreak > NUL

ECHO Launching Requester Node to execute a task...
start "Aegis Requester" cmd /k "python requester_node.py && pause"

ECHO.
ECHO Aegis network components launched.