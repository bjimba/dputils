@echo off

if defined dpdomain goto DomainOk
>&2 echo Please run dp-environ.bat first
goto :EOF

:DomainOk
>&2 echo Host: %dphost%
>&2 echo Domain: %dpdomain%
>&2 echo.

rem No arguments -- we'll use the current environment

setlocal
set tmpfile=%TMP%\tmp-get-status-services.xml

> %tmpfile% (
echo ^<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<env:Body^>
echo ^<dp:request xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:get-status class="ServicesStatus"/^>
echo ^</dp:request^>
echo ^</env:Body^>
echo ^</env:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current
