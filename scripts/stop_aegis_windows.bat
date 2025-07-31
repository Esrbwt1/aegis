@echo off
ECHO =======================================================
ECHO  AEGIS NETWORK TERMINATOR (WINDOWS)
ECHO =======================================================
ECHO.
ECHO Attempting to shut down all Uvicorn server processes...
ECHO.

taskkill /IM uvicorn.exe /F /T > NUL

ECHO.
ECHO All Aegis server components have been terminated.
ECHO You can manually close any remaining terminal windows.