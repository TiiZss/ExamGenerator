@echo off
setlocal EnableDelayedExpansion
title ExamGenerator Management Menu

:MENU
cls
echo ========================================================
echo               EXAMGENERATOR MANAGEMENT
echo ========================================================
echo.
echo   1. Start Environment (Local)
echo      [Launches Docker Stack: App + Web + DB]
echo.
echo   2. Deploy to Production
echo      [Uploads code to server and deploys]
echo.
echo   3. Docker Quickstart
echo      [Clean start without cache]
echo.
echo   4. Install Dependencies
echo      [Setup local python environment]
echo.
echo   5. Generate Secret Key
echo      [Create new Flask Secret Key]
echo.
echo   6. CLI Help
echo      [Show available ExamGenerator commands]
echo.
echo   0. Exit
echo.
echo ========================================================
set /p choice=Select an option [0-6]: 

if "%choice%"=="1" goto START
if "%choice%"=="2" goto DEPLOY
if "%choice%"=="3" goto QUICKSTART
if "%choice%"=="4" goto INSTALL
if "%choice%"=="5" goto SECRET
if "%choice%"=="6" goto CLI
if "%choice%"=="0" goto EXIT

echo Invalid option. Please try again.
timeout /t 2 >nul
goto MENU

:START
cls
call scripts\start.bat
echo.
pause
goto MENU

:DEPLOY
cls
echo Launching Deployment Script...
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1
echo.
pause
goto MENU

:QUICKSTART
cls
echo Launching Quickstart...
powershell -ExecutionPolicy Bypass -File scripts\docker-quickstart.ps1
echo.
pause
goto MENU

:INSTALL
cls
echo Installing Dependencies...
powershell -ExecutionPolicy Bypass -File scripts\install.ps1
echo.
pause
goto MENU

:SECRET
cls
echo Generating Secret Key...
python scripts\generate_secret.py
echo.
pause
goto MENU

:CLI
cls
python cli.py --help
echo.
pause
goto MENU

:EXIT
echo Goodbye!
exit /b 0
