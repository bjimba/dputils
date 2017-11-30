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
echo %0 ip-address
echo Notes:
echo.    ip-address - where is syslog-tcp host
echo Example:
echo.    %0 10.97.216.145
goto :EOF

:ArgsOk
setlocal
set remoteip=%1
set tmpfile=%TMP%\tmp-mylog-on.xml

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:modify-config^>
echo ^<LogTarget name="jimr-debug-log"^>
echo ^<mAdminState^>enabled^</mAdminState^>
echo ^<RemoteAddress^>%remoteip%^</RemoteAddress^>
echo ^</LogTarget^>
echo ^</dp:modify-config^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current | xmlpp -
