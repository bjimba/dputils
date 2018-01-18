@echo off
rem don't setlocal here!

if defined dpenviron goto EnvironOk
>&2 echo Please set dpenviron
exit /b 1

:EnvironOk
call %~dp0\%dpenviron%.properties.bat
exit /b 0
