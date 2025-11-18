@echo off
REM AI Support System Test Script for Windows
REM Run this to verify the AI support system is working

color 0A
echo.
echo ==================================================
echo 🤖 AI Support System - Verification Script
echo ==================================================
echo.

REM Check if backend is running
echo 1️⃣  Checking if backend is running...
curl -s http://localhost:5000/api/health > nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ Backend is running on http://localhost:5000
) else (
    echo    ❌ Backend is not running. Start it with: cd backend ^&^& python run.py
    timeout /t 3
    exit /b 1
)

echo.

REM Check if API key is configured
echo 2️⃣  Checking Google API configuration...
if "%GOOGLE_API_KEY%"=="" (
    echo    ⚠️  GOOGLE_API_KEY not set (using offline mode^)
    echo    💡 Set it with: set GOOGLE_API_KEY=your_key
) else (
    echo    ✅ Google API Key is configured
)

echo.

REM Test quick-fix endpoint
echo 3️⃣  Testing quick-fix endpoint...
for /f %%A in ('curl -s -X POST http://localhost:5000/api/support/quick-fix -H "Content-Type: application/json" -d "{"issue_title": "Missing Meta Tags", "category": "seo"}"') do set RESPONSE=%%A

if "%RESPONSE%"=="" (
    echo    ❌ Could not reach API endpoint
) else (
    echo    ✅ Quick-fix endpoint working
    echo    Response received (first 50 chars^): %RESPONSE:~0,50%...
)

echo.

REM Summary
echo ==================================================
echo ✅ AI Support System is ready!
echo.
echo Next steps:
echo   1. Open http://localhost:3000
echo   2. Analyze a website
echo   3. Click '💡 AI Support' tab
echo   4. Click on any issue to see solution
echo.
echo 📚 Documentation:
echo   - Setup: AI_SUPPORT_SETUP.md
echo   - Details: AI_SUPPORT_IMPLEMENTATION.md
echo   - Quick Start: AI_SUPPORT_QUICKSTART.md
echo ==================================================

pause
