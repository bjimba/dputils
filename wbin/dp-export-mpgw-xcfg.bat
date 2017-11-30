@echo off

if defined dpdomain goto DomainOk
echo Please run dp-env.bat first
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

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:do-export
echo.     format="XML" all-files="false" persisted="true" deployment-policy=""^>
echo.     ^<dp:user-comment^>Via jimr.us dputils^</dp:user-comment^>
echo.     ^<dp:object
echo.         class="MultiProtocolGateway"
echo.         name="%objname%"
echo.         ref-objects="true"
echo.         ref-files="false"
echo.         include-debug="false" /^>
echo ^</dp:do-export^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current ^
 | xml sel -T -t -v "//*[local-name()='file']" ^
 | base64 -d >%objname%.xcfg
