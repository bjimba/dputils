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
echo %0 mpgw-name
echo Notes:
echo.    mpgw-name - MPGW object name
echo Example:
echo.    %0 jimr-mpgw-base
goto :EOF

:ArgsOk
setlocal
set mpgw=%1
set tmpfile=%TMP%\tmp-probe-off.xml


> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:modify-config^>
echo ^<MultiProtocolGateway name="%mpgw%"^>
echo ^<DebugMode^>off^</DebugMode^>
echo ^</MultiProtocolGateway^>
echo ^</dp:modify-config^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current | xmlpp -
