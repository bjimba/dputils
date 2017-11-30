@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first
goto :EOF

:DomainOk
echo Host: %dphost%
echo Domain: %dpdomain%
echo.

if "%2"=="" goto Usage
if not exist %1 goto ArgsOk
echo File %1 already exists locally -- delete it yourself first!

:Usage
echo Usage:
echo %0 filename dpfiledir
echo Notes:
echo.    filename - just filename, no DOS path.  Used both on DP and DOS
echo.    dpfiledir - no filename, just dir
echo.    WON'T RUN IF DOS FILE EXISTS!
echo Example:
echo .   %0 identity.xsl local:///jimr
goto :EOF

:ArgsOk
setlocal
set winfilespec=%1
set dpfilespec=%2/%1
set tmpfile=%TMP%\tmp-get-file.xml

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:get-file name="%dpfilespec%" /^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

REM curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current ^
REM  | xml sel -T -t -v "//*[local-name()='file']" ^
REM  | fold -w 64 ^
REM  | openssl enc -d -base64 >%winfilespec%

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current ^
 | xml sel -T -t -v "//*[local-name()='file']" ^
 | base64 -d >%winfilespec%

rem debug
rem curl -kv -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current ^
rem | tee debug-resp.xml
rem
rem TODO - deal with
rem <?xml version="1.0" encoding="UTF-8"?>
rem <env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"><env:Body><dp:response xmlns:dp="http://www.datapower.com/schemas/management"><dp:result>Authentication failure</dp:result></dp:response></env:Body></env:Envelope>

