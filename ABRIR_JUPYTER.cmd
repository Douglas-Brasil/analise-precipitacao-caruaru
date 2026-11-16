@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0iniciar_jupyter.ps1"
if errorlevel 1 pause
