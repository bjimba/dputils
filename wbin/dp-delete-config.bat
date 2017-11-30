@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first
goto :EOF

:DomainOk
echo Host: %dphost%
echo Domain: %dpdomain%
echo.

if not "%1"=="" goto ArgsOk

:Usage
echo Usage:
echo %0 mpgwname
echo Notes:
echo.    mpgwname - name of MPGW
echo Example:
echo .   %0 my-mpgw-service
goto :EOF

:ArgsOk
setlocal
set objname=%1
set tmpfile=%TMP%\tmp-export.xml

rem look in xml-mgmt.xsd, AnyDeleteElement

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:del-config^>
echo ^<LogTarget name="del-test-log"/^>
echo ^</dp:del-config^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current ^
 | xml sel -T -t -v "//*[local-name()='file']" ^
 | fold -w 64 ^
 | base64 -d >%objname%.zip
