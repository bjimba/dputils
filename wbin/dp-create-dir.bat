@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first
goto :EOF

:DomainOk
echo Host: %dphost%
echo Domain: %dpdomain%
echo.

if "%1"=="" goto Usage
goto ArgsOk

:Usage
echo Usage:
echo %0 dpfiledir
echo Notes:
echo.    dpfiledir - directory to create on DataPower
echo Example:
echo .   %0 local:///jimr
goto :EOF

:ArgsOk
setlocal
set dpdirspec=%1
set tmpfile=%TMP%\tmp-create-dir.xml

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:do-action^>
echo ^<CreateDir^>
echo ^<Dir^>%dpdirspec%^</Dir^>
echo ^</CreateDir^>
echo ^</dp:do-action^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current | xmlpp -
