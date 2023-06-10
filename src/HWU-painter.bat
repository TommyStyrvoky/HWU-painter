@echo off
echo Is livery color menu selected in livery editor before starting ?
pause

python "%~dp0batchIO.py" "%~1"
Pause