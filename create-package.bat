@echo off
REM Automated Test Framework - Package Creator (Batch)

setlocal enabledelayedexpansion

set OUTPUT_DIR=%1
if "%OUTPUT_DIR%"==" set OUTPUT_DIR=.

echo.
echo ========================================================
echo   Automated Test Framework - Package Creator
echo ========================================================
echo.

REM Create output directory
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM Generate timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/" %%a in ('time /t') do (set mytime=%%a%%b)
set TIMESTAMP=%mydate%_%mytime%
set PACKAGE_NAME=automated-test-framework_%TIMESTAMP%
set ZIP_FILE=%OUTPUT_DIR%\%PACKAGE_NAME%.zip
set MD5_FILE=%OUTPUT_DIR%\%PACKAGE_NAME%.zip.md5

echo [OK] Package name: %PACKAGE_NAME%
echo [OK] Output directory: %OUTPUT_DIR%
echo.

echo Creating ZIP file...
REM Note: This requires 7-Zip or Windows 10+ built-in tar
powershell -Command "Add-Type -AssemblyName 'System.IO.Compression.FileSystem'; [System.IO.Compression.ZipFile]::CreateFromDirectory('.', '%ZIP_FILE%')"

if exist "%ZIP_FILE%" (
    echo [OK] ZIP file created: %ZIP_FILE%
) else (
    echo [ERROR] Failed to create ZIP file
    exit /b 1
)

echo.
echo ========================================================
echo   Package created successfully!
echo ========================================================
echo.
echo Output files:
echo   - %PACKAGE_NAME%.zip
echo   - %PACKAGE_NAME%_log.txt
echo.
echo Location: %OUTPUT_DIR%
echo.
echo Next steps:
echo   1. Upload the ZIP file
echo   2. Share for distribution
echo   3. Extract on target machine
echo.
