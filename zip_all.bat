@echo off

:: Define the name of the output zip file
set zipfile=archive.zip

:: Create the zip file using PowerShell's Compress-Archive cmdlet
powershell -Command "Compress-Archive -Path 'app', 'backend', 'preview', 'test', 'gruppo_o Requirements.md', 'LICENSE', 'Mockup.md', 'README.md', 'requirements.txt' -DestinationPath '%zipfile%'"

echo Files and folders have been zipped into %zipfile%.
pause
