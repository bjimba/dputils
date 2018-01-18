#!/usr/bin/env python
import sys
import os
import base64
import urllib2
import re
import datetime
import shutil
from urllib import quote_plus as urlquote


def cleanup():
    if os.path.exists(startDir+"/"+inProgFile):
        os.remove(startDir+"/"+inProgFile)
    if os.path.exists(svnExpDir):
        shutil.rmtree(svnExpDir)
    LOGFILE.close()



def getDomain(svnProj, env):
    startInd = 0
    endInd = 0
    domain = ''
    f=open('serviceDomains.xml','r')
    for line in f.readlines():
        if startInd == 0: 
            if ('<Service' in line.replace(' ','')) and ('name="'+svnProj+'"' in line.replace(' ','')):
                startInd = 1
                continue
        elif startInd == 1:
            #check if there is a Service end tag or the environment being searched
            if ('</Service' in line.replace(' ','')):
                endInd = 1
                break
            if ('<'+env+'>' in line.replace(' ','')):
                #domain = line.partition('<'+env+'>')[2].partition('<')[0]
                r = re.compile('<'+env+'>(.*?)</')
                m = r.search(line)
                domain = m.group(1)
                break
    return domain


def copyAllFiles(domain, deviceList):
    #loop through current directory, create folder, and copy file
    for subdir, dirs, files in os.walk('.'):
        #create directory on DataPower in case it does not already exist
        #nextDir = subdir.partition(".")[2]
        r1 = re.compile('(.*)\.(.*)')
        m = r1.search(subdir)
        nextDir = m.group(2) 
        newDir = "local:///"+nextDir
        createDirResp = createDir(newDir, domain, deviceList)
        logdata = "Copying all files from "+subdir+" to "+newDir+"\n"
        LOGFILE.write(logdata)
        rc = 00
        for file in files:
            fullpath = os.path.join(subdir, file)
            f = open(fullpath, 'r')
            fstr = f.read()
            dpPath = 'local:///'+f.name.replace("./", "/")
            encodedFile = base64.b64encode(fstr)
            f.close()
            sfResp = setFile(encodedFile, domain, dpPath, deviceList)
            if sfResp == 00:
                print "file "+f.name+" copied successfully to all devices"
            if sfResp == 01:
                print "file "+f.name+" failed to copy to some devices"
            if sfResp == 02:
                print "no file attempted to copy"
            if sfResp == 99:
                print "file "+f.name+"  failed to copy to all devices"
                rc = 99  
                return rc
            if rc < sfResp:
                rc = sfResp
    return rc



def setFile(b64File, domain, fileDest, deviceList):
    templateLoc = startDir+"/setfile.xml"
    setfileReq = open(templateLoc).read()
    setFileFinalReq = setfileReq.replace('%filename%', fileDest)
    setFileFinalReq = setFileFinalReq.replace('%b64file%', b64File)
    setFileFinalReq = setFileFinalReq.replace('%domain%', domain)
    resp = ''
    copySucc = 0
    copyFailed = 0
    
    for d in deviceList:
        somaUrl = "https://"+d+":5550/service/mgmt/current"
        req = urllib2.Request(url=somaUrl, data=setFileFinalReq)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Copying file "+fileDest+" to "+d
        logdata = "Copying file "+fileDest+" to "+d+"\n"
        LOGFILE.write(logdata)
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr+"\n")
        if not "result>OK<" in respStr:
            copyFailed += 1
            resp = resp+"ERROR:failed to copy file to "+d+"\n"
        else:
            copySucc += 1
            resp = resp+"file copied to "+d+"\n"
    if copySucc == 0 and copyFailed > 0:
        RC = 99
    if copyFailed == 0 and copySucc > 0:
        RC = 00
    if copyFailed > 0 and copySucc > 0:
        RC = 01
    if copyFailed == 0 and copySucc == 0:
        RC = 02 
    return RC 


def createDir(dpDir, domain, deviceList):
    templateLoc = startDir+"/createDir.xml"
    createDirReq = open(templateLoc).read()
    createDirFinalReq = createDirReq.replace('%dir%', dpDir)
    createDirFinalReq = createDirFinalReq.replace('%domain%', domain)
    resp = ''
    copySucc = 0
    copyFailed = 0
    for d in deviceList:
        somaUrl = "https://"+d+":5550/service/mgmt/current"
        req = urllib2.Request(url=somaUrl, data=createDirFinalReq)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Creating directory "+dpDir+" on "+d
        logdata = "Creating directory "+dpDir+" on "+d+"\n"
        LOGFILE.write(logdata)
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr+"\n")
        #Strip out all spaces to check the response
        respStrNoSpace = re.sub(r'\s', '', respStr)
        if not "result>OK<" in respStrNoSpace:
            copyFailed += 1
            resp = resp+"ERROR:failed create directory on "+d+"\n"
            logdata = "ERROR:failed create directory on "+d+"\n"
            LOGFILE.write(logdata)
        else:
            copySucc += 1
            resp = resp+"Directory created in "+d+"\n"
            logdata = "Directory created in "+d+"\n"
            LOGFILE.write(logdata)
    if copySucc == 0 and copyFailed > 0:
        RC = 99
    if copyFailed == 0 and copySucc > 0:
        RC = 00
    if copyFailed > 0 and copySucc > 0:
        RC = 01
    if copyFailed == 0 and copySucc == 0:
        RC = 02 
    return RC 




def doImport(b64File, domain, deviceList, deploymentPolicy, fileName):
    templateLoc = startDir+"/doImport.xml"
    doImportReq = open(templateLoc).read()
    doImportFinalReq = doImportReq.replace('%b64File%', b64File)
    doImportFinalReq = doImportFinalReq.replace('%domain%', domain)
    doImportFinalReq = doImportFinalReq.replace('%deploymentPolicy%', deploymentPolicy)
    resp = ''
    importSucc = 0
    importFailed = 0
    importWarn = 0 
    for d in deviceList:
        somaUrl = "https://"+d+":5550/service/mgmt/current"
        req = urllib2.Request(url=somaUrl, data=doImportFinalReq)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Deploying zip file "+fileName+ " to "+d+" Domain "+domain
        logdata = "Deploying zip file "+fileName+ " to "+d+" Domain "+domain+"\n"
        LOGFILE.write(logdata)
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr+"\n")
        if not "import-results" in respStr:
            importFailed += 1
            resp = resp+"ERROR:failed to import file to "+d+" domain "+domain+"\n"
            logdata = "ERROR:failed to import file to "+d+" domain "+domain+"\n"
            LOGFILE.write(logdata)
        else:
            importSucc += 1
            resp = resp+"ZIP deployed to "+d+" domain "+domain+"\n"
            logdata = "ZIP deployed to "+d+" domain "+domain+"\n"
            LOGFILE.write(logdata)
            if ('status="ERROR"' in respStr) or ('status="FAIL"' in respStr):
                resp = resp+"Warning! Some objects did not import successfully"+"\n"
                logdata = "Warning! Some objects did not import successfully"+"\n"
                LOGFILE.write(logdata)
                importWarn += 1


    #Set return codes as follows
    # 00 = All deployments succesfull
    # 01 = All Deployments were succesfull but some objects failed to import
    # 02 = Import was succesfull on some deveices and failed on some
    # 03 = Import was succesfull on some devices with some warnings and failed on some   
    # 04 = No imports were attempted   
    # 99 = all imports failed   

    if importSucc == 0 and importFailed > 0:
        # all deployments failed
        RC = 99
    if importFailed == 0 and importSucc > 0:
        # all deployments were succesfull
        RC = 00
        if importWarn > 0:
            # some imports had failed objects
            RC = 01 
    if importFailed > 0 and importSucc > 0:
        # Some imports were succesfull and some failed
        RC = 02
        if importWarn > 0:
           # some warnings on the sucessful imports 
            RC = 03
    if importFailed == 0 and importSucc == 0:
        # No imports at all
        RC = 04 

    return RC

def doBackup(domain, deviceList):
    templateLoc = startDir+"/doBackup.xml"
    doBackupReq = open(templateLoc).read()
    doBackupFinalReq = doBackupReq.replace('%domain%', domain)
    resp = ''
    backupSucc = 0
    backupFailed = 0
    for d in deviceList:
        somaUrl = "https://"+d+":5550/service/mgmt/current"
        req = urllib2.Request(url=somaUrl, data=doBackupFinalReq)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Backing up "+d+" Domain "+domain
        logdata = "Backing up "+d+" Domain "+domain+"\n"
        LOGFILE.write(logdata)
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr+"\n")
        if not "<dp:file>" in respStr:
            backupFailed += 1
            print "ERROR:failed to backup "+d+" domain "+domain+"\n"
            logdata = "ERROR:failed to backup "+d+" domain "+domain+"\n"
            LOGFILE.write(logdata)
        else:
            print "Backup of "+d+" domain "+domain+" successful"+"\n"
            backupSucc += 1
            # parse out the backup data from the response
            data = re.search(r"(?<=<dp:file>).*?(?=</dp:file>)", respStr).group(0)
            #write backup to a file 
            os.chdir(startDir+"/backups")
            FORMAT = '%Y%m%d%H%M%S' 
            filename = '%s_%s_%s' % (domain, d, datetime.datetime.now().strftime(FORMAT))
            FILE = open(filename,"w")
            FILE.write(data)
            FILE.close()
            logdata = "Device "+d+", domain "+domain+" successfully backed up to logs/"+filename+"\n"
            LOGFILE.write(logdata)


    #Set return codes as follows
    # 00 = All backups succesfull
    # 02 = Backup was succesfull on some deveices and failed on some
    # 03 = Import was succesfull on some devices with some warnings and failed on some   
    # 04 = No imports were attempted   
    # 99 = all imports failed   

    if backupSucc == 0 and backupFailed > 0:
        # all backups failed
        RC = 99
    if backupFailed == 0 and backupSucc > 0:
        # all backups were succesfull
        RC = 00
    if backupFailed > 0 and backupSucc > 0:
        # Some backups were succesfull and some failed
        RC = 02
    if backupFailed == 0 and backupSucc == 0:
        # No backups at all
        RC = 04 

    return RC

def saveConfig(domain, deviceList):
    templateLoc = startDir+"/saveConfig.xml"
    createDirReq = open(templateLoc).read()
    createDirFinalReq = createDirReq.replace('%domain%', domain)
    saveSucc = 0
    saveFailed = 0

    for d in deviceList:
        somaUrl = "https://"+d+":5550/service/mgmt/current"
        req = urllib2.Request(url=somaUrl, data=createDirFinalReq)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Saving config domain="+domain+" on "+d
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr+"\n")
        #Strip out all spaces to check the response
        respStrNoSpace = re.sub(r'\s', '', respStr)
        if not "result>OK<" in respStrNoSpace:
            saveFailed += 1
            resp = "ERROR:saveConfig failed for domain="+domain+" on device="+d+"\n"
            logdata = "ERROR:saveConfig failed for domain="+domain+" on device="+d+"\n"
            LOGFILE.write(logdata)
        else:
            saveSucc += 1
            resp = "saveConfig completed for domain="+domain+" on device="+d+"\n"
            logdata = "saveConfig completed for domain="+domain+" on device="+d+"\n"
            LOGFILE.write(logdata)
    if saveSucc == 0 and saveFailed > 0:
        RC = 99
    if saveFailed == 0 and saveSucc > 0:
        RC = 00
    if saveFailed > 0 and saveSucc > 0:
        RC = 01
    if saveFailed == 0 and saveSucc == 0:
        RC = 02 
    return RC 



#----------------------  START MAIN LOGIC ----------------------------------------------------


usage = 'USAGE:\ndeploy.py <environment> <svnPath after DataPower> <SVN-UID:pw> <DP-UID:pw>\nex. deploy.py SB "/Projects/NascoInterAct/Branches/Jun2012/ESB Claim Search Service" mySVNID:pw1 myDPUID:pw1\n'
envList = "Environments:\nSB = Sandbox\nDEV = Dev\nSIT = SIT\nUAT = UAT\nPP = PreProd\nDMZ = DMZ-Prod\nLAN = LAN-Prod\nESB = ESB-Prod"

if len(sys.argv) < 2:
    print usage 
    print envList 
    sys.exit()
elif sys.argv[1] == "help":
    print usage
    print envList
    sys.exit()
elif len(sys.argv) < 5:
    print usage
    print envList
    sys.exit()
else:
    envArg = sys.argv[1]
    prjPath = sys.argv[2]

if envArg == "SB":
    deviceList = ['10.71.6.239']
    env = "SB"
elif envArg == "DEV":
    deviceList = ['10.71.6.239', '10.71.1.27']
    env = "DEV"
elif envArg == "SIT":
    deviceList = ['10.71.6.239']
    env = "SIT"
elif envArg == "UAT":
    deviceList = ['10.71.6.239']
    env = "UAT"
elif envArg == "PP":
    deviceList = ['10.71.6.239']
    env = "PREPROD"
elif envArg == "DMZ":
    deviceList = ['10.71.6.239']
    env = "PROD"
elif envArg == "LAN":
    deviceList = ['10.71.6.239']
    env = "PROD"
elif envArg == "ESB":
    deviceList = ['10.71.6.239']
    env = "PROD"
else:
    print usage 
    print envList 
    sys.exit()

svnCreds = sys.argv[3]
dpCreds = sys.argv[4]
svnCredsSpl = str.split(svnCreds,":")
svnUid = svnCredsSpl[0]
svnPw = svnCredsSpl[1]
dpCredsSpl = str.split(svnCreds,":")
dpUid = dpCredsSpl[0]
dpPw = dpCredsSpl[1]
dpBasicAuth = base64.encodestring(dpCreds)

#strip off trailing and leading / in prjPath
if prjPath[0] == "/":
    prjPath = prjPath[1:]
if prjPath[len(prjPath) - 1] == "/":
    prjPath = prjPath[0:len(prjPath)-1]

prjPathSplit = prjPath.split('/')
svnUrl = "http://slda325d.corpads.local/svn/DataPower/"+prjPath
svnProj = prjPathSplit[1] 
subPrj = prjPathSplit[len(prjPathSplit) - 1] 
startDirEx = os.path.realpath(__file__)
startDir = os.path.dirname(startDirEx)
#get the domain to deploy to
domain = getDomain(svnProj, env)
if domain == '':
    print "No domain configuration found for "+svnProj+" and env "+env
    sys.exit()

#make sure another deployment is not in progress for this domain in this environment
inProgFile = domain+"_"+env+".inprogress"
if os.path.isfile(inProgFile):
    print "Another deployment is in progress for domain "+domain+" in Environment "+env+". Exiting script..."
    sys.exit()
else:
    FILE = open(inProgFile,"w")
    FILE.write("Deployment initiated by SVN user="+svnUid+" and DataPower user="+dpUid+" for project "+svnProj+" in progress") 
    FILE.close()
    
if not os.path.exists(startDir+"/temp"):
    os.makedirs(startDir+"/temp")
svnExpDir = startDir+"/temp/"+svnProj
#create the log file for this deployment
if not os.path.exists(startDir+"/logs"):
    os.makedirs(startDir+"/logs")
os.chdir(startDir+"/logs")
FORMAT = '%Y%m%d%H%M%S' 
filename = '%s_%s_%s' % (domain, env, datetime.datetime.now().strftime(FORMAT))
LOGFILE = open(filename,"w")
logdata = "Deployment initiated: \nDP UID = "+dpUid+"\nSVN UID="+svnUid+"\nEnvironment="+env+"\nSVN Path="+prjPath+"\nDataPower Domain="+domain+"\n"
LOGFILE.write(logdata)
 
#Backup domain on all devices
#create the log file for this deployment
if not os.path.exists(startDir+"/backups"):
    os.makedirs(startDir+"/backups")  
backupResp = doBackup(domain, deviceList)
logdata = "Backup RC= "+str(backupResp)+"\n"
LOGFILE.write(logdata)
if backupResp > 02:
    #No devices were backed up
    print "Backup of domains failed. Exiting script..."
    cleanup()
    sys.exit() 
    

#Export svn project to temp directory
if os.path.exists(svnExpDir):
    #remove the directory and contents from previous run
    shutil.rmtree(svnExpDir)
os.makedirs(svnExpDir) 
    
os.chdir(svnExpDir)
svnExportCmd = "svn export '"+svnUrl+"' --force --no-auth-cache --non-interactive --username '"+svnUid+"' --password "+re.escape(svnPw)
#svnExportCmd = "svn export '"+svnUrl+"' --force --username "+svnUid+" --password "+urlquote(svnPw)
os.system(svnExportCmd)
print "cur dir is:"+os.getcwd()
svnPath = svnExpDir+"/"+subPrj

#HINT: if the "find ./temp -type f -name "*.zip" | while read file;  do   echo "${file}: $(unzip -l "${file}" | egrep -ie 'xsl|xml|xsd|wsdl' | grep -v dp-aux)";  done" command shows anything other than "export.xml" files, you may have the same file being deployed twice (one copy within the zip and another copy outside the zip) which might cause a problem

#create a list of all folders that should be copied to DataPower
copyDirs = [svnPath+"/XSL", svnPath+"/XSD", svnPath+"/WTX", svnPath+"/XML", svnPath+"/"+env+"/XML"]

#loop through dirs list to copy 
for d in copyDirs:
    if not os.path.exists(d):
        print "Directory "+d+" not in project to copy"
        logdata = "Directory "+d+" not in project to copy"+"\n"
        LOGFILE.write(logdata)
    else:
        os.chdir(d)
        print "Copying files from "+d+" to all devices in "+env+" environment..."
        logdata = "Copying files from "+d+" to all devices in "+env+" environment..."+"\n"
        LOGFILE.write(logdata)
        copyFilesRC = copyAllFiles(domain, deviceList)
        if copyFilesRC == 00:
            print "all files in "+d+" copied successfully"
            logdata = "CopyFiles RC=00: All files in "+d+" copied successfully"+"\n"
            LOGFILE.write(logdata)
        if copyFilesRC == 01:
            print "some files in "+d+"  failed to copy"
            logdata = "CopyFiles RC=01: some files in "+d+"  failed to copy"+"\n"
            LOGFILE.write(logdata)
        if copyFilesRC == 02:
            print "no files in "+d+" were available to copy"
            logdata = "CopyFiles RC=02: no files in "+d+" were available to copy"+"\n"
            LOGFILE.write(logdata)
        if copyFilesRC == 99:
            print "all files in "+d+"  failed to copy"
            logdata = "CopyFiles RC=99: all files in "+d+"  failed to copy"+"\n"
            LOGFILE.write(logdata)  
            sys.exit(99)
        os.chdir(svnPath)

# Get the binary zip files to deploy
#first deploy the deployment policy for the appropriate environment
hasDP = "no"
dpName = ""

if not os.path.exists(svnPath+"/"+env+"/DeploymentPolicy"):
    print "No Deployment policy directory exists for the environment selected"
    logdata = "No Deployment policy directory exists for the environment selected"+"\n"
    LOGFILE.write(logdata)
else:
    hasDP = "yes"
    os.chdir(svnPath+"/"+env+"/DeploymentPolicy")

    for subdir, dirs, files in os.walk('.'):
        for file in files:
           fileName = file
           dpName = fileName.split(".")[0]
           f = open(file, 'rb')
           fbin = f.read()
           encodedFile = base64.b64encode(fbin)
           f.close()
           sfResp = doImport(encodedFile, domain, deviceList, "", f.name)
           if sfResp == 00:
               print "RC00: all objects successfully"
               logdata = "RC00: all objects successfully"+"\n"
               LOGFILE.write(logdata)
           if sfResp == 01:
               print "RC01: WARNING - some objects failed to import"
               logdata = "RC01: WARNING - some objects failed to import"+"\n"
               LOGFILE.write(logdata)
           if sfResp == 02:
               print "RC02: WARNING - Import failed on one or more devices"
               logdata = "RC02: WARNING - Import failed on one or more devices"+"\n"
               LOGFILE.write(logdata)
           if sfResp == 03:
               print "RC03: WARNING - Import failed on one or more devices and some objects failed to import on others "
               logdata = "RC03: WARNING - Import failed on one or more devices and some objects failed to import on others "+"\n"
               LOGFILE.write(logdata)
           if sfResp == 04:
               print "RC04: WARNING - No deployment policy files to import"
               logdata = "RC04: WARNING - No deployment policy files to import"+"\n"
               LOGFILE.write(logdata)
           if sfResp == 99:
               print "ERROR: all Deployment Policy imports failed! Exiting script...." 
               logdata = "ERROR: all Deployment Policy imports failed! Exiting Script..."+"\n"
               LOGFILE.write(logdata)
               LOGFILE.close() 
               sys.exit(99)

#deploy config zip files to DataPower
if not os.path.exists(svnPath+"/Config"):
    print "No Config directory for the current project"
    logdata = "No Config directory for the current project"+"\n"
    LOGFILE.write(logdata) 
else:
    os.chdir(svnPath+"/Config")

    for subdir, dirs, files in os.walk('.'):
        for file in files:
	    f = open(file, 'rb')
	    fbin = f.read()
	    encodedFile = base64.b64encode(fbin)
	    f.close()
	    sfResp = doImport(encodedFile, domain, deviceList, dpName, f.name)
            print "sfResp is:"+str(sfResp)
            if sfResp == 00:
                print "RC00: all objects successfully imported on all devices"
                logdata = "RC00: all objects successfully imported on all devices"+"\n"
                LOGFILE.write(logdata) 
            if sfResp == 01:
                print "RC01: WARNING - some objects failed to import"
                logdata = "RC01: WARNING - some objects failed to import"+"\n"
                LOGFILE.write(logdata)  
            if sfResp == 02:
                print "RC02: WARNING - Import failed on one or more devices"
                logdata = "RC02: WARNING - Import failed on one or more devices"+"\n"
                LOGFILE.write(logdata)
            if sfResp == 03:
                print "RC03: WARNING - Import failed on one or more devices and some objects failed to import on others "
                logdata = "RC03: WARNING - Import failed on one or more devices and some objects failed to import on others "+"\n"
                LOGFILE.write(logdata)
            if sfResp == 04:
                print "RC04: WARNING - No config files to import"
                logdata = "RC04: WARNING - No config files to import"+"\n"
                LOGFILE.write(logdata)
            if sfResp == 99:
                print "ERROR: all config imports failed! Exiting Script..."
                logdata = "ERROR: all config imports failed! Exiting Script..."+"\n"
                LOGFILE.write(logdata)
                LOGFILE.close()
                sys.exit(99)

#persist the changes to datapower
saveConfigRC = saveConfig(domain, deviceList)
if saveConfigRC == 00:
    print "RC00: Configuration saved on all devices"
    logdata = "RC00: all Configuration saved on all devices"+"\n"
    LOGFILE.write(logdata) 
if saveConfigRC  == 01:
    print "RC01: WARNING - Save config failed on some devices"
    logdata = "RC01: WARNING - Save config failed on some devices"+"\n"
    LOGFILE.write(logdata)  
if saveConfigRC  == 02:
    print "RC02: WARNING - No save configuration attempted on any devices"
    logdata = "RC02: WARNING - No save configuration attempted on any devices"+"\n"
    LOGFILE.write(logdata)
if saveConfigRC  == 99:
    print "ERROR: Save configuration failed on all devices!"
    logdata = "ERROR: Save configuration failed on all devices!"+"\n"
    LOGFILE.write(logdata)
    LOGFILE.close()
    sys.exit(99)

#call cleanup function and sys.exit script
cleanup()
sys.exit()

