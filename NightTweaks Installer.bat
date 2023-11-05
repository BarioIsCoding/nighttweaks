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

REM Copy token.txt to the target folder
if exist "token.txt" (
    copy "token.txt" "%targetFolder%"
    echo Copied "token.txt" to "%targetFolder%"
)

REM Create a shortcut on the desktop
set "shortcutName=NightTweaks.lnk"
set "shortcutTarget=%targetFolder%\NightTweaks.py"
set "desktopFolder=%userprofile%\Desktop"

REM Check if the shortcut already exists
if not exist "%desktopFolder%\%shortcutName%" (
    echo Creating shortcut on the desktop...
    echo Set WshShell = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
    echo Set objShortcut = WshShell.CreateShortcut("%desktopFolder%\%shortcutName%") >> CreateShortcut.vbs
    echo objShortcut.TargetPath = "%shortcutTarget%" >> CreateShortcut.vbs
    echo objShortcut.Save >> CreateShortcut.vbs
    cscript CreateShortcut.vbs
    del CreateShortcut.vbs
    echo Shortcut created on the desktop: "%desktopFolder%\%shortcutName%"
) else (
    echo Shortcut already exists on the desktop: "%desktopFolder%\%shortcutName%"
)

REM Install required Python modules
echo Installing required Python modules...
pip install discord==1.7.3
pip install urllib3
pip install tqdm
pip install asyncio
pip install re
pip install tkinter

echo Done.
pause
