@echo off

if defined dpdomain goto DomainOk
echo Please run dp-env.bat first
goto :EOF

:DomainOk
echo Host: %dphost%
echo Domain: %dpdomain%
echo.

if not "%2"=="" goto ArgsOk

:Usage
echo Usage:
echo %0 xcfg-filespec deploy-policy
echo Notes:
echo.    xcfg-filespec - filename of object XCFG
echo.    deploy-policy - name of deployment policy ^(use 'NONE' if not needed^)
echo Example:
echo .   %0 my-object.xcfg DIGITAL_deployPolicy
goto :EOF

:ArgsOk
setlocal
set xcfgfilespec=%1
set dpolicy=%2
if "%2" == "NONE" set dpolicy=
set tmpfile=%TMP%\tmp-import.xml

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
echo.     deployment-policy="%dpolicy%"^>
echo      ^<dp:input-file
echo | set /p dummy=">"
base64 -e %xcfgfilespec%
echo ^</dp:input-file^>
echo ^</dp:do-import^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current | xmlpp -
