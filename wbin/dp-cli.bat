@echo off

if defined dpdomain goto DomainOk
echo Please run dp-env.bat first
goto :EOF

:DomainOk
echo Host: %dphost%
echo Domain: %dpdomain%
echo.

setlocal
plink -ssh %dphost%
