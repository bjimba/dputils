@echo off

if not "%1"=="" goto ArgsOk
if not defined dpenviron goto Usage

echo Current DP environment - %dpenviron%
echo Current dputils dir - %~dp0
echo.

:Usage
echo Usage:
echo %0 environ-name
echo.
echo environ-name can be:
echo sandbox dp-dock dp-mock dev-vm
echo dev-east dev-west1 dev-west2 dev-west3
echo sit-east
echo sit-west1 sit-west11 sit-west12
echo sit-west2 sit-west21 sit-west22
echo pt-east pt-east1 pt-east2
echo pt-west pt-west1 pt-west2
echo prod-east prod-east1 prod-east2 prod-west prod-west1 prod-west2
goto :EOF

:ArgsOk
if "%1"=="sandbox" goto Sandbox
if "%1"=="dp-dock" goto DpDock
if "%1"=="dp-dock2" goto DpDock2
if "%1"=="dp-dock10" goto DpDock10
if "%1"=="dp-build" goto DpBuild
if "%1"=="dp-mock" goto DpMock
if "%1"=="dp-mock2" goto DpMock2
if "%1"=="dp-mock3" goto DpMock3
if "%1"=="dp-mock4" goto DpMock4
if "%1"=="dp-mock5" goto DpMock5
if "%1"=="dev-vm" goto DevVm
if "%1"=="dev-east" goto DevEast
if "%1"=="dev-west1" goto DevWest1
if "%1"=="dev-west2" goto DevWest2
if "%1"=="dev-west3" goto DevWest3
if "%1"=="sit-east" goto SitEast
if "%1"=="sit-eastp" goto SitEastP
if "%1"=="sit-west1" goto SitWest1
if "%1"=="sit-west11" goto SitWest11
if "%1"=="sit-west11a" goto SitWest11a
if "%1"=="sit-west11p" goto SitWest11p
if "%1"=="sit-west12" goto SitWest12
if "%1"=="sit-west12a" goto SitWest12a
if "%1"=="sit-west12p" goto SitWest12p
if "%1"=="sit-west2" goto SitWest2
if "%1"=="sit-west21" goto SitWest21
if "%1"=="sit-west21a" goto SitWest21a
if "%1"=="sit-west21p" goto SitWest21p
if "%1"=="sit-west22" goto SitWest22
if "%1"=="sit-west22a" goto SitWest22a
if "%1"=="sit-west22p" goto SitWest22p
if "%1"=="sit-west3" goto SitWest3
if "%1"=="sit-west31" goto SitWest31
if "%1"=="sit-west31p" goto SitWest31p
if "%1"=="sit-west32" goto SitWest32
if "%1"=="sit-west32p" goto SitWest32p
if "%1"=="pt-east" goto PtEast
if "%1"=="pt-east-oneway" goto PtEastOneWay
if "%1"=="pt-east1" goto PtEast1
if "%1"=="pt-east2" goto PtEast2
if "%1"=="pt-west" goto PtWest
if "%1"=="pt-west1" goto PtWest1
if "%1"=="pt-west2" goto PtWest2
if "%1"=="prod-east" goto ProdEast
if "%1"=="prod-east1" goto ProdEast1
if "%1"=="prod-east1a" goto ProdEast1a
if "%1"=="prod-east2" goto ProdEast2
if "%1"=="prod-east2a" goto ProdEast2a
if "%1"=="prod-east5" goto ProdEast5
if "%1"=="prod-east6" goto ProdEast6
if "%1"=="prod-west" goto ProdWest
if "%1"=="prod-west1" goto ProdWest1
if "%1"=="prod-west1a" goto ProdWest1a
if "%1"=="prod-west2" goto ProdWest2
if "%1"=="prod-west2a" goto ProdWest2a
if "%1"=="prod-west5" goto ProdWest5
if "%1"=="prod-west6" goto ProdWest6
goto Usage

:Sandbox
set dpenviron=sandbox
rem host only
rem set dphost=192.168.109.128
rem nat
rem set dphost=192.168.16.128
rem new dpvm601
set dphost=192.168.16.130
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=sandbox
set dpuid=jrussell
set dppwd=markcare
set prompt=[%dpenviron%] $p$g
goto :EOF

:DpDock
set dpenviron=dp-dock
set dphost=10.124.30.30
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=jimr
set dppwd=altcare
rem set dpgatewaytype=no-tls
rem set dpgatewayport=4850
set dpgatewaytype=twoway
set dpgatewayport=4851
rem set dpgatewaytype=oneway
rem set dpgatewayport=4852
set prompt=[%dpenviron%] $p$g
goto :EOF

:DpDock2
set dpenviron=dp-dock2
set dphost=10.124.30.30
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL2
set dpuid=jimr
set dppwd=markcare
rem set dpgatewaytype=no-tls
rem set dpgatewayport=4850
set dpgatewaytype=twoway
set dpgatewayport=4851
rem set dpgatewaytype=oneway
rem set dpgatewayport=4852
set prompt=[%dpenviron%] $p$g
goto :EOF

:DpDock10
set dpenviron=dp-dock10
set dphost=10.124.30.30
set dpxml=%dphost%
set dpxmlport=10550
set dpdomain=DBPLICE
set dpuid=jimr
set dppwd=markcare
rem set dpgatewaytype=no-tls
rem set dpgatewayport=10850
set dpgatewaytype=twoway
set dpgatewayport=10851
rem set dpgatewaytype=oneway
rem set dpgatewayport=10852
set prompt=[%dpenviron%] $p$g
goto :EOF

:DpBuild
set dpenviron=dp-build
set dphost=10.228.129.48
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=dpbuild
set dppwd=dpmaster
set dpgatewaytype=twoway
set dpgatewayport=4851
set prompt=[%dpenviron%] $p$g
goto :EOF

:DpMock
set dpenviron=dp-mock
rem set dphost=10.105.172.199
rem set dphost=10.105.172.140
set dphost=10.105.172.59
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=dpuser
set dppwd=dpusergo
set prompt=[%dpenviron%] $p$g
goto :EOF

:DpMock2
set dpenviron=dp-mock2
rem set dphost=10.105.172.199
rem set dphost=10.105.172.140
rem set dphost=10.105.172.59
set dphost=paz1psyss2l39v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=dpuser
set dppwd=dpusergo
set prompt=[%dpenviron%] $p$g
goto :EOF

:DpMock3
set dpenviron=dp-mock3
set dphost=paz1psyss3l31v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=dpuser
set dppwd=dpusergo
set prompt=[%dpenviron%] $p$g
goto :EOF

:DpMock4
set dpenviron=dp-mock4
set dphost=paz1psyss3l32v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=dpuser
set dppwd=dpusergo
set prompt=[%dpenviron%] $p$g
goto :EOF

:DpMock5
set dpenviron=dp-mock5
set dphost=paz1psyss3l34v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=dpuser
set dppwd=dpusergo
set prompt=[%dpenviron%] $p$g
goto :EOF

:DevVm
set dpenviron=dev-vm
set dphost=192.168.16.130
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=jrussell
set dppwd=markcare
set prompt=[%dpenviron%] $p$g
goto :EOF

:DevEast
set dpenviron=dev-east
set dphost=rri2esladp1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:DevWest1
set dpenviron=dev-west1
set dphost=paz1esladp1v.caremarkrx.net
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:DevWest2
set dpenviron=dev-west2
set dphost=paz1eslad2p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:DevWest3
set dpenviron=dev-west3
set dphost=paz1eslad3p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
rem set dpgatewaytype=twoway
rem set dpgatewayport=4026
set dpgatewaytype=no-tls
set dpgatewayport=4812
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitEast
set dpenviron=sit-east
set dphost=rri2eslatp1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitEastP
set dpenviron=sit-eastp
set dphost=rri2eslatp1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=probe
set dppwd=p@ssw0rd!
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest1
set dpenviron=sit-west1
set dphost=esldp-sit1-west.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest11
set dpenviron=sit-west11
set dphost=paz1eslas1p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest11a
set dpenviron=sit-west11a
set dphost=paz1eslas1p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
rem set dpuid=8960773
rem set dppwd=Sora22pina!
set dpuid=8954997
set dppwd=Lovegod!168
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest11p
set dpenviron=sit-west11p
set dphost=paz1eslas1p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=probe
set dppwd=p@ssw0rd!
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest12
set dpenviron=sit-west12
set dphost=paz1eslas1p2v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest12a
set dpenviron=sit-west12a
set dphost=paz1eslas1p2v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=8960773
set dppwd=Sora22pina!
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest12p
set dpenviron=sit-west12p
set dphost=paz1eslas1p2v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=probe
set dppwd=p@ssw0rd!
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest2
set dpenviron=sit-west2
set dphost=esldp-sit2-west.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
rem set dpgatewaytype=no-tls
rem set dpgatewayport=4233
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest21
set dpenviron=sit-west21
set dphost=paz1eslas2p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest21a
set dpenviron=sit-west21a
set dphost=paz1eslas2p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=8954997
set dppwd=Lovegod!168
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest21p
set dpenviron=sit-west21p
set dphost=paz1eslas2p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=probe
set dppwd=p@ssw0rd!
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest22
set dpenviron=sit-west22
set dphost=paz1eslas2p2v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest22a
set dpenviron=sit-west22a
set dphost=paz1eslas2p2v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=8954997
set dppwd=Lovegod!168
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest22p
set dpenviron=sit-west22p
set dphost=paz1eslas2p2v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=probe
set dppwd=p@ssw0rd!
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest3
set dpenviron=sit-west3
set dphost=esldp-sit3-west.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPLICE
set dpuid=1320276
set dppwd=Friday22#
rem set dpgatewaytype=no-tls
rem set dpgatewayport=4233
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest31
set dpenviron=sit-west31
set dphost=paz1eslas3p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPLICE
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest31p
set dpenviron=sit-west31p
set dphost=paz1eslas3p1v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPLICE
set dpuid=probe
set dppwd=p@ssw0rd!
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest32
set dpenviron=sit-west32
set dphost=paz1eslas3p2v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPLice
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest32p
set dpenviron=sit-west32p
set dphost=paz1eslas3p2v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPLICE
set dpuid=probe
set dppwd=p@ssw0rd!
set prompt=[%dpenviron%] $p$g
goto :EOF

:SitWest22a
set dpenviron=sit-west22a
set dphost=paz1eslas2p2v.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=8954997
set dppwd=Lovegod!168
set prompt=[%dpenviron%] $p$g
goto :EOF

:PtEast
set dpenviron=pt-east
rem set dphost=esldp-pt-east.corp.cvscaremark.com
set dphost=dbpldp-pt-east.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:PtEastOneWay
set dpenviron=pt-east-oneway
rem set dphost=esldp-pt-east.corp.cvscaremark.com
set dphost=dbpldp-pt-east.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=oneway
set dpgatewayport=4811
set prompt=[%dpenviron%] $p$g
goto :EOF

:PtEast1
set dpenviron=pt-east1
set dphost=rri2eslanp1p.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:PtEast2
set dpenviron=pt-east2
set dphost=rri2eslanp2p.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:PtWest
set dpenviron=pt-west
rem set dphost=esldp-pt-west.corp.cvscaremark.com
set dphost=dbpldp-pt-west.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:PtWest1
set dpenviron=pt-west1
set dphost=paz1eslapep1p-mgt.caremarkrx.net
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:PtWest2
set dpenviron=pt-west2
set dphost=paz1eslapep2p-mgt.caremarkrx.net
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdEast
set dpenviron=prod-east
rem set dphost=esldp-east.corp.cvscaremark.com
set dphost=dbpldp-east.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdEast1
set dpenviron=prod-east1
set dphost=rri2eslapp1p.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdEast1a
set dpenviron=prod-east1a
set dphost=rri2eslapp1p.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=8954997
set dppwd=Lovegod!168
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdEast2
set dpenviron=prod-east2
rem set dphost=rri2eslapp2p.corp.cvscaremark.com
set dphost=rri2eslapp2p-sec.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdEast2a
set dpenviron=prod-east2a
set dphost=rri2eslapp2p.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=8954997
set dppwd=Lovegod!168
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdEast5
set dpenviron=prod-east5
set dphost=rri2eslapp5p.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdEast6
set dpenviron=prod-east6
set dphost=rri2eslapp6p.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdWest
set dpenviron=prod-west
rem set dphost=esldp-west.corp.cvscaremark.com
set dphost=dbpldp-west.corp.cvscaremark.com
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set dpgatewaytype=twoway
set dpgatewayport=4026
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdWest1
set dpenviron=prod-west1
set dphost=paz1eslapp1p-mgt.caremarkrx.net
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdWest1a
set dpenviron=prod-west1a
set dphost=paz1eslapp1p-mgt.caremarkrx.net
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
REM set dpuid=8960773
REM set dppwd=Sora22pina!
set dpuid=8954997
set dppwd=Lovegod!168
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdWest2
set dpenviron=prod-west2
set dphost=paz1eslapp2p-mgt.caremarkrx.net
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdWest2a
set dpenviron=prod-west2a
set dphost=paz1eslapp2p-mgt.caremarkrx.net
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=8954997
set dppwd=Lovegod!168
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdWest5
set dpenviron=prod-west5
set dphost=paz1eslapp5p-mgt.caremarkrx.net
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

:ProdWest6
set dpenviron=prod-west6
set dphost=paz1eslapp6p-mgt.caremarkrx.net
set dpxml=%dphost%
set dpxmlport=5550
set dpdomain=DBPL
set dpuid=1320276
set dppwd=Friday22#
set prompt=[%dpenviron%] $p$g
goto :EOF

