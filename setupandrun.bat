@echo off
setlocal

REM Download and extract portable Python
echo Downloading portable Python...
curl -LO https://www.python.org/ftp/python/3.10.0/python-3.10.0-embed-amd64.zip
mkdir python
tar -xf python-3.10.0-embed-amd64.zip -C python

REM Add Python to PATH
set PATH=%CD%\python;%PATH%

REM Install pip
echo Installing pip...
curl -LO https://bootstrap.pypa.io/get-pip.py
python\python.exe get-pip.py

REM Install packages from requirements.txt
echo Installing required packages...
python\python.exe -m pip install -r requirements.txt

REM Open two command windows to run lms.py and run-uv.py
echo Starting lms.py and run-uv.py in separate command windows...
start cmd /k python\python.exe lms.py
start cmd /k python\python.exe run-uv.py

echo All tasks completed.
endlocal
pause
