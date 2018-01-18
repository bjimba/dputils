#!/usr/bin/ksh

cat $0

targetEnv=$1
deploySrc=$2
credsDir=$3

. $credsDir/scriptcreds

./deploy.py "${targetEnv}" "${deploySrc}" "${svnuid}":"${svnpw}" "${dpuid}":"${dppw}"
