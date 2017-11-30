@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first
goto :EOF

:DomainOk
1>&2 (
echo Host: %dphost%
echo Domain: %dpdomain%
echo.
)

if not "%1"=="" goto ArgsOk

1>&2 (
echo Usage:
echo %0 dplocation
echo Notes:
echo.    dplocation - local:, cert:, etc.  Colon required!
echo Example:
echo .   %0 local:
)
goto :EOF

:ArgsOk
setlocal
set dplocation=%1
set tmpfile=%TMP%\tmp-get-filestore.xml

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:get-filestore location="%dplocation%" /^>
REM echo ^<dp:get-filestore /^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current
