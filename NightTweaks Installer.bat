@echo off
setlocal

REM Define the target folder path
set "targetFolder=C:\Users\%USERNAME%\AppData\Roaming\!!NightTweaks"

REM Create the target folder if it doesn't exist
if not exist "%targetFolder%" (
    mkdir "%targetFolder%"
)

REM Define the list of allowed file names
set "allowedFiles=EmbedGenerator.html NightTweaks Installer.bat NightTweaks.py README.md index.html"

REM Loop through the files in the current directory
for %%F in (%allowedFiles%) do (
    if exist "%%~F" (
        move "%%~F" "%targetFolder%"
        echo Moved "%%~F" to "%targetFolder%"
    )
)

echo Done.
pause
