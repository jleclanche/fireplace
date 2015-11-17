@echo off
@where Powershell.exe
if %ERRORLEVEL% neq 0 (
	echo Please install Powershell from https://www.microsoft.com/en-us/download/details.aspx?id=40855
) ELSE (
	Powershell.exe -executionpolicy remotesigned -File bootstrap.ps1
)

