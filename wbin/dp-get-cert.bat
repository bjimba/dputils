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
set dpcc=%1

rem step 1: run cc-export on dp box
call dp-crypto-export %dpcc%

rem step 2: pull the generated cert
rm %dpcc%.xml
call dp-get-file %dpcc%.xml temporary:///

rem step 3: turn it into a PEM cert
> %dpcc%.pem.cer (
echo -----BEGIN CERTIFICATE-----
xmllint --xpath "/crypto-export/certificate/text()" %dpcc%.xml
echo.
echo -----END CERTIFICATE-----
)

rem step 4: show me the carfax
cat %dpcc%.pem.cer

