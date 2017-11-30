@echo off

if defined dpdomain goto DomainOk
echo Please run dp-environ.bat first
goto :EOF

:DomainOk
echo Host: %dphost%
echo Domain: %dpdomain%
echo.

rem if not "%1"=="" goto ArgsOk
rem no args
goto ArgsOk

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
rem set objname=%1
set tmpfile=%TMP%\tmp-modify-ssparam.xml

> %tmpfile% (
echo ^<?xml version="1.0" encoding="UTF-8"?^>
echo ^<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"^>
echo ^<soapenv:Body^>
echo ^<dp:request
echo.    xmlns:dp="http://www.datapower.com/schemas/management"
echo.    domain="%dpdomain%"^>
echo ^<dp:modify-config^>
echo ^<StylePolicyAction name="jimr-rule-req-ssparams_xform_0"^>
echo ^<StylesheetParameters^>
echo   ^<ParameterName^>BackendUrl^</ParameterName^>
echo   ^<ParameterValue^>http://xyzzy.us^</ParameterValue^>
echo ^</StylesheetParameters^>
rem echo ^<StylesheetParameters^>
rem echo   ^<ParameterName^>env^</ParameterName^>
rem echo   ^<ParameterValue^>jimr-xyzzy^</ParameterValue^>
rem echo ^</StylesheetParameters^>
echo ^</StylePolicyAction^>
echo ^<MultiProtocolGateway name="DIGITAL_MPGW_CON_Preferences"^>
echo ^<DebugMode^>on^</DebugMode^>
echo ^</MultiProtocolGateway^>
echo ^</dp:modify-config^>
echo ^</dp:request^>
echo ^</soapenv:Body^>
echo ^</soapenv:Envelope^>
)

curl -k -u %dpuid%:%dppwd% -d @%tmpfile% https://%dpxml%:%dpxmlport%/service/mgmt/current | xmlpp -
