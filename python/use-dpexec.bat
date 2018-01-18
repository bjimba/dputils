@echo off
setlocal

rem try using dpexec to deploy

rem set dpenv=dock10
set dpenv=sandbox

call dpexec %dpenv% getstatusfirmware

pushd %my_home%\devel\gitlab\datapower-dbpl-experimental

rem upload files
cd local
call dpexec %dpenv% sendtree ICEM

rem upload certs
cd ../cert
call dpexec %dpenv% setfile eadl1v-2019-key-pw.pem cert:///
call dpexec %dpenv% setfile eadl1v-2019-cert.pem.cer cert:///

rem upload sharedcerts
cd ../sharedcert
call dpexec %dpenv% setfile alphassl-g2-sha1-2022-04-13.pem.cer sharedcert:///
call dpexec %dpenv% setfile alphassl-g2-sha256-2024-02-20.pem.cer sharedcert:///
call dpexec %dpenv% setfile symantec-g3-sha256-2023-10-30.pem.cer sharedcert:///
call dpexec %dpenv% setfile symantec-g4-sha256-2023-10-30.pem.cer sharedcert:///
call dpexec %dpenv% setfile verisign-g3-sha1-2020-02-07.pem.cer sharedcert:///

rem upload dpconfig
cd ..\dpconfig
call dpexec %dpenv% doImportXcfg DIGITAL_deployPolicy.xcfg NONE

rem upload common objects
rem XMLMGR_Local
call dpexec %dpenv% doImportXcfg edit-xmlmgr-local.xcfg NONE
rem crypto?

rem deploy mpgws
call dpexec --verbose %dpenv% doImportXcfg clean-getDashBoardDataJSON.xcfg DIGITAL_deployPolicy

popd

