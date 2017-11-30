@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first
goto :EOF

:DomainOk
echo Host: %dphost%
echo Domain: %dpdomain%
echo.

rem No arguments -- work off current dpdomain

setlocal
set tmpfile=%TMP%\tmp-do-backup.xml

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"^>
echo ^<dp:do-backup format="ZIP"^>
echo.     ^<dp:domain name="%dpdomain%"/^>
echo ^</dp:do-backup^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current ^
 >resp-do-backup.xml

rem | xml sel -T -t -v "//*[local-name()='file']" ^
rem | fold -w 64 ^
rem | base64 -d >backup-%dpdomain%.zip
