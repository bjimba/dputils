import dpxml

dp_host = 'localhost'
dp_domain = 'jimr'
dp_creds = 'jimr:NancyWh1.'

dpx = dpxml.dpxml(host=dp_host, domain=dp_domain, creds=dp_creds)
dpx.port = '5551'

# rmsg will be 'OK' on success

# create a directory on DP
#rmsg = dpx.createDir('local:///newdir')
# backup a domain to a local ZIP
rmsg = dpx.doBackup('backup.zip')
# import configuration ZIP
rmsg = dpx.doImport('config.zip')
# import configuration ZIP using existing DeployPol
rmsg = dpx.doImport('config.zip', 'deploypolicy-name')
# persist running config
rmsg = dpx.saveConfig()
# upload file to DP
rmsg = dpx.setFile('this-file.xyz', 'local:///directory')
# upload directory tree to DP local:///
rmsg = sendTreeToDpLocal('c:/myfiles/dpwork')

