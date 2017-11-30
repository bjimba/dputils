@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first 1>&2
goto :EOF

:DomainOk
1>&2 (
echo Host: %dphost%
echo Domain: %dpdomain%
echo.
)

if "%2"=="" goto Usage
if not exist %1 goto Usage
if not exist %2 goto Usage
goto ArgsOk

:Usage
1>&2 (
echo Usage:
echo %0 zip1 zip2
echo Notes:
echo.    zip1 and zip2 are the two Datapower ZIP exports to compare
echo Example:
echo .   %0 x.zip y.zip
)
goto :EOF

:ArgsOk
setlocal
set zip1=%1
set zip2=%2
set tmpfile=%TMP%\tmp-get-diff.xml
set tmpresp=%TMP%\tmp-get-diff-resp.xml

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:get-diff^>
echo ^<dp:from^>
echo ^<dp:export
echo | set /p dummy=">"
base64 -e %zip1%
echo ^</dp:export^>
echo ^</dp:from^>
echo ^<dp:to^>
echo ^<dp:export
echo | set /p dummy=">"
base64 -e %zip2%
echo ^</dp:export^>
echo ^</dp:to^>
echo ^</dp:get-diff^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current >%tmpresp%
xsltproc %~dp0\filter-get-diff.xsl %tmpresp%
