@echo off

set .=%~dp0

"%.%py_3.11.9.x64/python.exe" "%.%script.py"

if %errorlevel% neq 0 (
    echo.
    echo Something went wrong! You may want to take a screenshot and send it to 1j2n3k4m5g7dev@gmail.com  .
)

echo.
pause