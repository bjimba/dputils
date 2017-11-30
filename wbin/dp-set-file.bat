@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first
goto :EOF

:DomainOk
echo Host: %dphost%
echo Domain: %dpdomain%
echo.

if "%2"=="" goto Usage
if exist %1 goto ArgsOk
echo File %1 does not exist!

:Usage
echo Usage:
echo %0 sourcefilename dpfiledir
echo Notes:
echo.    sourcefile - just filename, no DOS path
echo.    dpfiledir - no filename, just dir
echo.    For full path/renames, use dp-set-file-fullpaths instead
echo Example:
echo .   %0 identity.xsl local:///jimr
goto :EOF

:ArgsOk
setlocal
set winfilespec=%1
set dpfilespec=%2/%1
set tmpfile=%TMP%\tmp-set-file.xml

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:set-file name="%dpfilespec%"
echo | set /p dummy=">"
base64 -e %winfilespec%
echo ^</dp:set-file^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current | xmlpp -
