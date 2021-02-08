@echo off
title .UI to .py files converter !
echo Generate Python files from .UI files!
echo ""
echo Start Converting Files Please wait.


cd /Forms
call pyuic5 engCalcForm.ui -o engCalcUI.py

@REM echo QRC file Name
@REM set /p QrName=Enter .qrc file Name: 
@REM echo ""
@REM echo ""
@REM echo ""
@REM echo ""
@REM echo PY file Name
@REM set /p PiName=Enter .PY file Name: 
@REM echo ""
@REM echo ""
@REM echo ""
@REM echo Start Converting Files Please wait.

@REM pyrcc5 -o "%PiName%" "%QrName%"

echo Job Completed.
