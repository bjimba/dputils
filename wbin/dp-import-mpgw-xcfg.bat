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
set tmpfile=%TMP%\tmp-import.xml
set xcfgfilespec=%objname%.xcfg

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:do-import
echo.     source-type="XML"
echo.     dry-run="false"
echo.     overwrite-files="false"
echo.     overwrite-objects="true"
echo.     rewrite-local-ip="false"
echo.     deployment-policy="DIGITAL_deployPolicy"^>
echo      ^<dp:input-file
echo | set /p dummy=">"
base64 -e %xcfgfilespec%
echo ^</dp:input-file^>
rem echo.     ^<dp:object
rem echo.         class="MultiProtocolGateway"
rem echo.         name="%objname%"
rem echo.         overwrite="true"
rem echo.         import-debug="false" /^>
echo ^</dp:do-import^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current | xmlpp -
