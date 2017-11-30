@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first
goto :EOF

:DomainOk
1>&2 (
echo Host: %dphost%
echo Domain: %dpdomain%
echo.
)

rem No arguments -- work off current dpdomain

setlocal
set tmpfile=%TMP%\tmp-get-status-tcptable.xml

> %tmpfile% (
echo ^<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<env:Body^>
echo ^<dp:request xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:get-status class="TCPTable"/^>
echo ^</dp:request^>
echo ^</env:Body^>
echo ^</env:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current
