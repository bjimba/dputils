@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first
goto :EOF

:DomainOk
echo Host: %dphost%
echo Domain: %dpdomain%
echo.

if not "%1"=="" goto ArgsOk
echo Usage:
echo %0 xml-mgr
goto :EOF

:ArgsOk
setlocal
set xmlmgr=%1
set tmpfile=%TMP%\tmp-flush-document-cache.xml

> %tmpfile% (
echo ^<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<env:Body^>
echo ^<dp:request xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:do-action^>
echo ^<FlushDocumentCache^>
echo ^<XMLManager^>%xmlmgr%^</XMLManager^>
echo ^</FlushDocumentCache^>
echo ^</dp:do-action^>
echo ^</dp:request^>
echo ^</env:Body^>
echo ^</env:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current
