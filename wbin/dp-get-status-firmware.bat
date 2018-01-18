@echo off
setlocal

call %~dp0\dp-init.bat
if errorlevel 1 goto :EOF

echo dpenviron %dpenviron%
echo host %host%
goto :EOF

rem This could either call FirmwareStatus or FirmwareVersion
rem FirmwareVersion seems more useful

:DomainOk
>&2 echo Host: %dphost%
>&2 echo Domain: %dpdomain%
>&2 echo.

rem No arguments -- we'll use the current environment

setlocal
set tmpfile=%TMP%\tmp-get-status-firmware.xml

> %tmpfile% (
echo ^<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<env:Body^>
echo ^<dp:request xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:get-status class="FirmwareVersion"/^>
echo ^</dp:request^>
echo ^</env:Body^>
echo ^</env:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current
