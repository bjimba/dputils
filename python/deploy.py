#!/usr/bin/env python
import sys
import os
import base64
import urllib2
import re
import datetime
import shutil
from urllib import quote_plus as urlquote

# global space - constants (may move to config)
svnBase = "http://slda325d.corpads.local/svn/DataPower/"
somaUrlTemplate = "https://%host%:5550/service/mgmt/current"

# envdict - info based on environment arg
#   key = envArg
#   value = [ 'env', 'name', [devlist] ]
envdict = {
    'SB':  [ 'SB',      'Sandbox',  ['10.71.6.239']],
    'DEV': [ 'DEV',     'Dev',      ['10.71.6.239', '10.71.1.27']],
    'SIT': [ 'SIT',     'SIT',      ['10.71.6.239']],
    'UAT': [ 'UAT',     'UAT',      ['10.71.6.239']],
    'PP':  [ 'PREPROD', 'PreProd',  ['10.71.6.239']],
    'DMZ': [ 'PROD',    'DMZ-Prod', ['10.71.6.239']],
    'LAN': [ 'PROD',    'LAN-Prod', ['10.71.6.239']],
    'ESB': [ 'PROD',    'ESB-Prod', ['10.71.6.239']] }

def UsageExit():
    print """USAGE:
deploy.py <environment> <svnPath after DataPower> <SVN-UID:pw> <DP-UID:pw>
ex. deploy.py SB "Projects/NascoInterAct/Branches/Jun2012/ESB Claim Search Service" mySVNID:pw1 myDPUID:pw1
"""
    print "Environments:"
    for k, v in envdict.items():
        print k + ' = ' + v[1]

    sys.exit(1)

# global space - paths and files
baseDir = ''
logDir = ''
tmpDir = ''
backupDir = ''
inProgFile = ''

def SetPaths():
    # baseDir assumed already set
    # let's try to always have '/' at end of directory paths
    if baseDir[len(base)-1] != '/':
        baseDir += '/'
    logDir = baseDir + 'logs/'
    tmpDir = baseDir + 'temp/'
    backupDir = baseDir + 'backups/'

class UidPwd:
    """ expect string uid:pwd at creation time """
    def __init__(self, cred):
        self.cred = cred
        split = str.split(cred, ":")
        self.uid = split[0]
        self.pwd = split[1]
    def getUid(self):
        return self.uid
    def getPwd(self):
        return self.pwd
    def getB64Cred(self):
        return base64.encodestring(self.cred)

def removeIfExists(fspec):
    if os.path.exists(fspec):
        os.remove(fspec)
def rmdirIfExists(path):
    if os.path.exists(path):
        shutil.rmtree(path)
def mkdirIfNeeded(path):
    if not os.path.exists(path):
        os.makedirs(path)

def cleanup():
    removeIfExists(inProgFile)
    rmdirIfExists(svnExpDir)
    LOGFILE.close()

# implement using minidom
def getDomain(svnProj, env):
    import xml.dom.minidom as xdm
    doc = xdm.parse('serviceDomains.xml')
    serviceNodes = doc.getElementsByTagName('Service')
    dpDomain = ''
    for serviceNode in serviceNodes:
        if svnProj == serviceNode.getAttribute('name'):
            envNode = serviceNode.getElementsByTagName(env)[0]
            dpDomain = str(envNode.firstChild.nodeValue)
    return dpDomain

def sendTreeToDpLocal(domain, deviceList):
    # send tree at current directory to Datapower local:///

    for subdir, dirs, files in os.walk('.'):

        # we're walking down tree, starting at cwd
        # at each step:
        #   assume subdir is already on DP (since we start at '.', and create [ dirs ])
        #   create any dirs in [ dirs ]
        #   send any file in [ files ]

        currdir = subdir
        # chop off initial './' (one at a time since root is '.')
        if '.' == currdir[0]: currdir = currdir[1:]
        if '/' == currdir[0]: currdir = currdir[1:]

        rc = 0
        for dir in dirs:
            localdir = 'local:///' + currdir + '/' + dir
            rc = dpCreateDir(currdir, domain, deviceList)
            # we should make use of rc

        logdata = "Copying all files from " + subdir + " to dp local:///" + currdir + "\n"
        LOGFILE.write(logdata)

        rc = 00
        for file in files:
            fullpath = os.path.join(currdir, file)
            f = open(fullpath, 'r')
            fstr = f.read()
            encodedFile = base64.b64encode(fstr)
            f.close()

            dpPath = 'local:///' + currdir + '/' + file
            sfResp = dpSetFile(encodedFile, domain, dpPath, deviceList)
            if sfResp == 00:
                print "file " + f.name + " copied successfully to all devices"
            if sfResp == 01:
                print "file " + f.name + " failed to copy to some devices"
            if sfResp == 02:
                print "no file attempted to copy"
            if sfResp == 99:
                print "file " + f.name + "  failed to copy to all devices"
                rc = 99
                return rc
            if rc < sfResp:
                rc = sfResp
    return rc

def createXmlFromTemplate(templateFspec, paramDict):
    xml = open(templateFspec).read()
    for k, v in paramDict.items():
        xml = xml.replace('%' + k + '%', v)
    return xml

def dpSetFile(b64File, domain, fileDest, deviceList):

    reqXml = createXmlFromTemplate(baseDir + 'setfile.xml',
        {   'filename': fileDest,
            'b64file': b64File,
            'domain': domain })

    resp = ''
    copySucc = 0
    copyFailed = 0

    for d in deviceList:
        somaUrl = somaUrlTemplate.replace('%host%', d)
        req = urllib2.Request(url=somaUrl, data=reqXml)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Copying file " + fileDest + " to " + d
        logdata = "Copying file " + fileDest + " to " + d + "\n"
        LOGFILE.write(logdata)
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr + "\n")
        if not "result>OK<" in respStr:
            copyFailed += 1
            resp = resp + "ERROR:failed to copy file to " + d + "\n"
        else:
            copySucc += 1
            resp = resp + "file copied to " + d + "\n"
    if copySucc == 0 and copyFailed > 0:
        RC = 99
    if copyFailed == 0 and copySucc > 0:
        RC = 00
    if copyFailed > 0 and copySucc > 0:
        RC = 01
    if copyFailed == 0 and copySucc == 0:
        RC = 02
    return RC


def dpCreateDir(dpDir, domain, deviceList):
    reqXml = createXmlFromTemplate(baseDir + 'createDir.xml',
        {   'dir': dpDir,
            'domain': domain })
    resp = ''
    copySucc = 0
    copyFailed = 0
    for d in deviceList:
        somaUrl = somaUrlTemplate.replace('%host%', d)
        req = urllib2.Request(url=somaUrl, data=reqXml)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Creating directory " + dpDir + " on " + d
        logdata = "Creating directory " + dpDir + " on " + d + "\n"
        LOGFILE.write(logdata)
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr + "\n")
        #Strip out all spaces to check the response
        respStrNoSpace = re.sub(r'\s', '', respStr)
        if not "result>OK<" in respStrNoSpace:
            copyFailed += 1
            resp = resp + "ERROR:failed create directory on " + d + "\n"
            logdata = "ERROR:failed create directory on " + d + "\n"
            LOGFILE.write(logdata)
        else:
            copySucc += 1
            resp = resp + "Directory created in " + d + "\n"
            logdata = "Directory created in " + d + "\n"
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

def dpDoImport(b64File, domain, deviceList, deploymentPolicy, fileName):
    reqXml = createXmlFromTemplate(baseDir + 'doImport.xml',
        {   'b64File': b64File,
            'domain': domain,
            'deploymentPolicy', deploymentPolicy })

    resp = ''
    importSucc = 0
    importFailed = 0
    importWarn = 0
    for d in deviceList:
        somaUrl = somaUrlTemplate.replace('%host%', d)
        req = urllib2.Request(url=somaUrl, data=reqXml)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Deploying zip file " + fileName +  " to " + d + " Domain " + domain
        logdata = "Deploying zip file " + fileName +  " to " + d + " Domain " + domain + "\n"
        LOGFILE.write(logdata)
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr + "\n")
        if not "import-results" in respStr:
            importFailed += 1
            resp = resp + "ERROR:failed to import file to " + d + " domain " + domain + "\n"
            logdata = "ERROR:failed to import file to " + d + " domain " + domain + "\n"
            LOGFILE.write(logdata)
        else:
            importSucc += 1
            resp = resp + "ZIP deployed to " + d + " domain " + domain + "\n"
            logdata = "ZIP deployed to " + d + " domain " + domain + "\n"
            LOGFILE.write(logdata)
            if ('status="ERROR"' in respStr) or ('status="FAIL"' in respStr):
                resp = resp + "Warning! Some objects did not import successfully" + "\n"
                logdata = "Warning! Some objects did not import successfully" + "\n"
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

def dpDoBackup(domain, deviceList):
    reqXml = createXmlFromTemplate(baseDir + 'doBackup.xml',
        { 'domain': domain })
    resp = ''
    backupSucc = 0
    backupFailed = 0
    for d in deviceList:
        somaUrl = somaUrlTemplate.replace('%host%', d)
        req = urllib2.Request(url=somaUrl, data=reqXml)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Backing up " + d + " Domain " + domain
        logdata = "Backing up " + d + " Domain " + domain + "\n"
        LOGFILE.write(logdata)
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr + "\n")
        if not "<dp:file>" in respStr:
            backupFailed += 1
            print "ERROR:failed to backup " + d + " domain " + domain + "\n"
            logdata = "ERROR:failed to backup " + d + " domain " + domain + "\n"
            LOGFILE.write(logdata)
        else:
            print "Backup of " + d + " domain " + domain + " successful" + "\n"
            backupSucc += 1
            # parse out the backup data from the response
            data = re.search(r"(?<=<dp:file>).*?(?=</dp:file>)", respStr).group(0)
            #write backup to a file
            os.chdir(backupDir)
            FORMAT = '%Y%m%d%H%M%S'
            filename = '%s_%s_%s' % (domain, d, datetime.datetime.now().strftime(FORMAT))
            FILE = open(filename,"w")
            FILE.write(data)
            FILE.close()
            logdata = "Device " + d + ", domain " + domain + " successfully backed up to logs/" + filename + "\n"
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
    reqXml = createXmlFromTemplate(baseDir + 'saveConfig.xml',
        { 'domain': domain }
    saveSucc = 0
    saveFailed = 0

    for d in deviceList:
        somaUrl = somaUrlTemplate.replace('%host%', d)
        req = urllib2.Request(url=somaUrl, data=reqXml)
        req.add_header("Authorization", "Basic %s" % dpBasicAuth)
        print "Saving config domain=" + domain + " on " + d
        respStr = urllib2.urlopen(req).read()
        LOGFILE.write(respStr + "\n")
        #Strip out all spaces to check the response
        respStrNoSpace = re.sub(r'\s', '', respStr)
        if not "result>OK<" in respStrNoSpace:
            saveFailed += 1
            resp = "ERROR:saveConfig failed for domain=" + domain + " on device=" + d + "\n"
            logdata = "ERROR:saveConfig failed for domain=" + domain + " on device=" + d + "\n"
            LOGFILE.write(logdata)
        else:
            saveSucc += 1
            resp = "saveConfig completed for domain=" + domain + " on device=" + d + "\n"
            logdata = "saveConfig completed for domain=" + domain + " on device=" + d + "\n"
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

if __name__ == "__main__":

    if len(sys.argv) < 5:
        UsageExit()
    if sys.argv[1] == "help":
        UsageExit()

    envArg = sys.argv[1]
    if not envArg in envdict:
        UsageExit()
    env = envdict[envArg][0]
    deviceList = envdict[envArg][2]

    prjPath = sys.argv[2]

    svnCred = UidPwd(sys.argv[3])
    svnUid = svnCred.getUid()
    svnPw = svnCred.getPwd()

    dpCred = UidPwd(sys.argv[4])
    dpUid = dpCred.getUid()
    dpBasicAuth = dpCred.getB64Cred()

    #strip off trailing and leading / in prjPath
    if prjPath[0] == "/":
        prjPath = prjPath[1:]
    if prjPath[len(prjPath) - 1] == "/":
        prjPath = prjPath[0:len(prjPath)-1]

    # project arg - expect 'Projects/proj/.../subproj'
    # - will end up deploying all in subproj to DP local://proj/

    prjPathSplit = prjPath.split('/')
    svnUrl = svnBase + prjPath
    svnProj = prjPathSplit[1]
    subPrj = prjPathSplit[len(prjPathSplit) - 1]

    # base path is where the script itself lives
    baseDir = os.path.realpath(os.path.dirname(sys.argv[0]))

    # baseDir is global - SetPaths will set other paths relative to it
    # everything else will be underneath this
    SetPaths()
    # let's try to stay in base dir most of the time
    os.chdir(baseDir)

    #get the domain to deploy to (from XML config)
    domain = getDomain(svnProj, env)
    if domain == '':
        print "No domain configuration found for " + svnProj + " and env " + env
        sys.exit(1)

    #make sure another deployment is not in progress for this domain in this environment
    inProgFile = baseDir + domain + "_" + env + ".inprogress"
    if os.path.isfile(inProgFile):
        print "Another deployment is in progress for domain " + domain + " in Environment " + env + ". Exiting script..."
        sys.exit(1)

    FILE = open(inProgFile, "w")
    FILE.write("Deployment initiated by SVN user=" + svnUid + " and DataPower user=" + dpUid + " for project " + svnProj + " in progress")
    FILE.close()

    mkdirIfNeeded(tmpDir)
    svnExpDir = tmpDir + svnProj

    # create the log file for this deployment
    mkdirIfNeeded(logDir)
    # jpr - we shouldn't have to cwd here
    #os.chdir(logDir)
    FORMAT = '%Y%m%d%H%M%S'
    filename = '%s_%s_%s' % (domain, env, datetime.datetime.now().strftime(FORMAT))
    LOGFILE = open(logDir + filename, "w")
    logdata = 'Deployment initiated: \n'
    logdata += 'DP UID = ' + dpUid + '\n'
    logdata += 'SVN UID=' + svnUid + '\n'
    logdata +' Environment=' + env + '\n'
    logdata += 'SVN Path=' + prjPath + '\n'
    logdata += 'DataPower Domain=' + domain + '\n'
    LOGFILE.write(logdata)

    #Backup domain on all devices
    mkdirIfNeeded(backupDir)
    backupResp = dpDoBackup(domain, deviceList)
    logdata = "Backup RC= " + str(backupResp) + "\n"
    LOGFILE.write(logdata)
    if backupResp > 02:
        #No devices were backed up
        print "Backup of domains failed. Exiting script..."
        cleanup()
        sys.exit(1)

    #Export svn project to temp directory
    rmdirIfExists(svnExpDir)
    os.makedirs(svnExpDir)

    # we have to chdir here, since svn doesn't provide an output-target option
    os.chdir(svnExpDir)
    svnExportCmd = "svn export"
    svnExportCmd += " '" + svnUrl + "'"
    #svnExportCmd += " --force"
    svnExportCmd += " --force --no-auth-cache --non-interactive"
    #svnExportCmd += " --username '" + svnUid + "' --password " + urlquote(svnPw)
    svnExportCmd += " --username '" + svnUid + "' --password " + re.escape(svnPw)
    os.system(svnExportCmd)
    print "cur dir is:" + os.getcwd()
    svnPath = svnExpDir + "/" + subPrj

    #HINT: if the
    #       find ./temp -type f -name "*.zip" \
    #       | while read file; \
    #           do echo "${file}: $(unzip -l "${file}" | egrep -ie 'xsl|xml|xsd|wsdl' | grep -v dp-aux)"; \
    #       done
    # command shows anything other than "export.xml" files, you may have the same file being deployed twice
    # (one copy within the zip and another copy outside the zip) which might cause a problem

    # jpr - this shouldn't be hard-coded
    #create a list of all folders that should be copied to DataPower
    copyDirs = [svnPath + "/XSL",
        svnPath + "/XSD",
        svnPath + "/WTX",
        svnPath + "/XML",
        svnPath + "/" + env + "/XML"]

    #loop through dirs list to copy
    for d in copyDirs:
        if not os.path.exists(d):
            print "Directory " + d + " not in project to copy"
            logdata = "Directory " + d + " not in project to copy" + "\n"
            LOGFILE.write(logdata)
        else:
            os.chdir(d)
            print "Copying files from " + d + " to all devices in " + env + " environment..."
            logdata = "Copying files from " + d + " to all devices in " + env + " environment..." + "\n"
            LOGFILE.write(logdata)

            copyFilesRC = sendTreeToDpLocal(domain, deviceList)

            if copyFilesRC == 00:
                print "all files in " + d + " copied successfully"
                logdata = "CopyFiles RC=00: All files in " + d + " copied successfully" + "\n"
                LOGFILE.write(logdata)
            if copyFilesRC == 01:
                print "some files in " + d + "  failed to copy"
                logdata = "CopyFiles RC=01: some files in " + d + "  failed to copy" + "\n"
                LOGFILE.write(logdata)
            if copyFilesRC == 02:
                print "no files in " + d + " were available to copy"
                logdata = "CopyFiles RC=02: no files in " + d + " were available to copy" + "\n"
                LOGFILE.write(logdata)
            if copyFilesRC == 99:
                print "all files in " + d + "  failed to copy"
                logdata = "CopyFiles RC=99: all files in " + d + "  failed to copy" + "\n"
                LOGFILE.write(logdata)
                sys.exit(99)
            os.chdir(svnPath)

    # Get the binary zip files to deploy
    #first deploy the deployment policy for the appropriate environment
    hasPolicy = "no"
    dpName = ""

    if not os.path.exists(svnPath + "/" + env + "/DeploymentPolicy"):
        print "No Deployment policy directory exists for the environment selected"
        logdata = "No Deployment policy directory exists for the environment selected" + "\n"
        LOGFILE.write(logdata)
    else:
        hasPolicy = "yes"
        os.chdir(svnPath + "/" + env + "/DeploymentPolicy")

        # is walk needed here? we don't seem to look at subdirs
        for subdir, dirs, files in os.walk('.'):
            for file in files:
                fileName = file
                dpName = fileName.split(".")[0]
                f = open(file, 'rb')
                fbin = f.read()
                encodedFile = base64.b64encode(fbin)
                f.close()
                sfResp = dpDoImport(encodedFile, domain, deviceList, "", f.name)
                if sfResp == 00:
                    print "RC00: all objects successfully"
                    logdata = "RC00: all objects successfully" + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 01:
                    print "RC01: WARNING - some objects failed to import"
                    logdata = "RC01: WARNING - some objects failed to import" + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 02:
                    print "RC02: WARNING - Import failed on one or more devices"
                    logdata = "RC02: WARNING - Import failed on one or more devices" + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 03:
                    print "RC03: WARNING - Import failed on one or more devices and some objects failed to import on others "
                    logdata = "RC03: WARNING - Import failed on one or more devices and some objects failed to import on others " + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 04:
                    print "RC04: WARNING - No deployment policy files to import"
                    logdata = "RC04: WARNING - No deployment policy files to import" + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 99:
                    print "ERROR: all Deployment Policy imports failed! Exiting script...."
                    logdata = "ERROR: all Deployment Policy imports failed! Exiting Script..." + "\n"
                    LOGFILE.write(logdata)
                    LOGFILE.close()
                    sys.exit(99)

    #deploy config zip files to DataPower
    if not os.path.exists(svnPath + "/Config"):
        print "No Config directory for the current project"
        logdata = "No Config directory for the current project" + "\n"
        LOGFILE.write(logdata)
    else:
        os.chdir(svnPath + "/Config")

        for subdir, dirs, files in os.walk('.'):
            for file in files:
                # scan here for local files in zip? Maybe
                # z = zipfile.ZipFile(file)
                # zlist = z.namelist()
                # look through namelist for 'local/xxx'
                f = open(file, 'rb')
                fbin = f.read()
                encodedFile = base64.b64encode(fbin)
                f.close()
                sfResp = dpDoImport(encodedFile, domain, deviceList, dpName, f.name)
                print "sfResp is:" + str(sfResp)
                if sfResp == 00:
                    print "RC00: all objects successfully imported on all devices"
                    logdata = "RC00: all objects successfully imported on all devices" + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 01:
                    print "RC01: WARNING - some objects failed to import"
                    logdata = "RC01: WARNING - some objects failed to import" + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 02:
                    print "RC02: WARNING - Import failed on one or more devices"
                    logdata = "RC02: WARNING - Import failed on one or more devices" + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 03:
                    print "RC03: WARNING - Import failed on one or more devices and some objects failed to import on others "
                    logdata = "RC03: WARNING - Import failed on one or more devices and some objects failed to import on others " + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 04:
                    print "RC04: WARNING - No config files to import"
                    logdata = "RC04: WARNING - No config files to import" + "\n"
                    LOGFILE.write(logdata)
                if sfResp == 99:
                    print "ERROR: all config imports failed! Exiting Script..."
                    logdata = "ERROR: all config imports failed! Exiting Script..." + "\n"
                    LOGFILE.write(logdata)
                    LOGFILE.close()
                    sys.exit(99)

    #persist the changes to datapower
    saveConfigRC = saveConfig(domain, deviceList)
    if saveConfigRC == 00:
        print "RC00: Configuration saved on all devices"
        logdata = "RC00: all Configuration saved on all devices" + "\n"
        LOGFILE.write(logdata)
    if saveConfigRC  == 01:
        print "RC01: WARNING - Save config failed on some devices"
        logdata = "RC01: WARNING - Save config failed on some devices" + "\n"
        LOGFILE.write(logdata)
    if saveConfigRC  == 02:
        print "RC02: WARNING - No save configuration attempted on any devices"
        logdata = "RC02: WARNING - No save configuration attempted on any devices" + "\n"
        LOGFILE.write(logdata)
    if saveConfigRC  == 99:
        print "ERROR: Save configuration failed on all devices!"
        logdata = "ERROR: Save configuration failed on all devices!" + "\n"
        LOGFILE.write(logdata)
        LOGFILE.close()
        sys.exit(99)

    #call cleanup function and sys.exit script
    cleanup()
    sys.exit(0)

