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
echo %0 dpcryptocert
echo Notes:
echo.    dpcryptocert
echo Example:
echo .   %0 MyCCObject
goto :EOF

:ArgsOk
setlocal
set dpcryptocert=%1
set tmpfile=%TMP%\tmp-crypto-export.xml

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:do-action^>
echo ^<CryptoExport^>
echo ^<ObjectType^>cert%^</ObjectType^>
echo ^<ObjectName^>%dpcryptocert%^</ObjectName^>
echo ^<OutputFilename^>%dpcryptocert%.xml^</OutputFilename^>
echo ^</CryptoExport^>
echo ^</dp:do-action^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current | xmlpp -
