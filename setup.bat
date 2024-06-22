@echo off
SETLOCAL

:: Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed on your system.
    echo Please download and install Python from https://www.python.org/downloads/
    pause
    exit /b
) ELSE (
    echo Python is already installed.
)

:: Check if virtualenv is installed
pip show virtualenv >nul 2>&1
IF ERRORLEVEL 1 (
    echo virtualenv is not installed. Installing virtualenv...
    pip install virtualenv
)

:: Create a virtual environment if it doesn't exist
IF NOT EXIST "evm_wallet_scanner_env" (
    echo Creating virtual environment...
    virtualenv evm_wallet_scanner_env
)

:: Activate the virtual environment
call evm_wallet_scanner_env\Scripts\activate

:: Check if required libraries are installed
pip show web3 mnemonic rich requests >nul 2>&1
IF ERRORLEVEL 1 (
    echo Required libraries are not installed. Installing libraries...
    pip install web3 mnemonic rich requests
)

:: Run the main script
echo Activating the virtual environment and running the script...
python main.py

ENDLOCAL
