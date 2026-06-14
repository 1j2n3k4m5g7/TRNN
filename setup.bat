@echo off

set .=%~dp0

"%.%py_3.11.9.x64/python.exe" -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo. Something went wrong!
)

echo.
pause