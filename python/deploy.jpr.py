#!/usr/bin/env python
import base64
import datetime
import logging
import os
import re
import shutil
import sys

import dpxml
import dpdeploy_cfg as cfg


def UsageExit():
    print """USAGE:
deploy.py <environment> <svnPath after DataPower> <SVN-UID:pw> <DP-UID:pw>
ex. deploy.py SB "Projects/MemberCreate/Branches/May2013/ESB Enterprise Member Create Service" mySVNID:pw1 myDPUID:pw1
"""
    print "Environments:"
    for k, v in cfg.envs.items():
        print k + ' = ' + v.friendly_name

    sys.exit(1)

class UidPwd:
    """ expect string uid:pwd at creation time """
    def __init__(self, cred):
        self.cred = cred
        split = str.split(cred, ":")
        self.uid = split[0]
        self.pwd = split[1]
    def getCred(self):
        return self.cred
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
    # scope???
    removeIfExists(inProgFile)
    rmdirIfExists(svnExpDir)


if __name__ == "__main__":

    logger = logging.getLogger()

    if len(sys.argv) < 5:
        UsageExit()
    if sys.argv[1] == "help":
        UsageExit()

    env_arg = sys.argv[1]
    if not env_arg in cfg.envs:
        UsageExit()
    svn_env = cfg.envs[env_arg].svn_env
    hosts = cfg.envs[env_arg].hosts

    project_path = sys.argv[2]
    svn_cred = UidPwd(sys.argv[3])
    dp_cred = UidPwd(sys.argv[4])

    #strip off trailing and leading / in project_path
    if project_path[0] == "/":
        project_path = project_path[1:]
    if project_path[len(project_path) - 1] == "/":
        project_path = project_path[0:len(project_path)-1]

    # project arg - expect 'Projects/proj/.../service'
    # - will end up deploying all in service to DP local://proj/

    path_split = project_path.split('/')
    svnUrl = cfg.svn_base + project_path
    svn_project = path_split[1]
    svn_service = path_split[len(path_split) - 1]

    # base path is where the script itself lives
    # - set other paths relative to it
    base_dir = os.path.realpath(os.path.dirname(sys.argv[0]))
    if base_dir[len(base)-1] != '/':
        base_dir += '/'
    logDir = base_dir + 'logs/'
    tmpDir = base_dir + 'temp/'
    backupDir = base_dir + 'backups/'

    # let's try to stay in base dir most of the time
    os.chdir(base_dir)

    # get the domain to deploy to (from XML config)
    dp_domain = cfg.get_dp_domain(svn_project, svn_env)
    if dp_domain == '':
        print "No domain configuration found for " + svn_project + " and env " + svn_env
        sys.exit(1)

    # make sure another deployment is not in progress for this domain in this environment
    # jpr: this seems wrong - we should block if there is an inProgress for *any* env/domain, since
    #   they all use the same svn temp dir!

    inProgFile = "%s%s_%s.inprogress" %(base_dir, dp_domain, svn_env)
    if os.path.isfile(inProgFile):
        print "Another deployment is in progress for domain %s in Environment %s. Exiting script..." %(dp_domain, svn_env)
        sys.exit(1)
    f = open(inProgFile, "w")
    f.write("Deployment initiated by SVN user=%s and DataPower user=%s for project %s in progress" %(
        svn_cred.getUid(), dp_cred.getUid(), svn_project))
    f.close()

    # logging - two logging handlers - a file in logDir and console
    #   (lets us set the level differently for each)
    mkdirIfNeeded(logDir)
    logFspec = '%s%s_%s_%s' %(
        logDir, dp_domain, svn_env, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    lhFile = logging.FileHandler(logFspec)
    lhFile.setLevel(logging.DEBUG)
    lhConsole = logging.StreamHandler()
    lhConsole.setLevel(logging.INFO)
    lFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    lhFile.setFormatter(lFormat)
    lhConsole.setFormatter(lFormat)
    logger.addHandler(lhFile)
    logger.addHandler(lhConsole)

    logger.info('Deployment initiated:')
    logger.info('DP UID = %s' % dp_cred.getUid())
    logger.info('SVN UID=%s' % svn_cred.getUid())
    logger.info(' Environment=%s' % svn_env)
    logger.info('SVN Path=%s' % project_path)
    logger.info('DataPower Domain=%' % dp_domain)

    #Backup domain on all devices

    mkdirIfNeeded(backupDir)

    for dpHost in devicelist:
        dpx = dpxml.dpxml(host=dpHost, domain=dp_domain, creds=dp_cred.getCred())
        fspec = "%s%s_%s_%s.zip" %(
            backupDir, dp_domain, dpHost, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        rmsg = dpx.doBackup(fspec)
        if rmsg != "OK":
            logger.error("Backup of domains failed. Exiting script...")
            cleanup()
            sys.exit(1)

    #Export svn project to temp directory
    mkdirIfNeeded(tmpDir)
    svnExpDir = tmpDir + svn_project
    rmdirIfExists(svnExpDir)
    os.makedirs(svnExpDir)

    # we have to chdir here, since svn doesn't provide an output-target option
    os.chdir(svnExpDir)
    cmd = "svn export '%s' --force --no-auth-cache --non-interactive --username '%s' --password %s" %(
            svnUrl, svn_cred.getUid(), re.escape(svn_cred.getPwd()))
    os.system(cmd)
    print "cur dir is:" + os.getcwd()
    svnPath = svnExpDir + "/" + svn_service

    # create a list of all folders that should be copied to DataPower local:///
    copyDirs = [svnPath + "/XSL",
        svnPath + "/XSD",
        svnPath + "/WTX",
        svnPath + "/XML",
        svnPath + "/" + svn_env + "/XML"]

    for host in hostlist:

        # copy files to local
        for copyDir in copyDirs:
            if not os.path.exists(copyDir):
                logger.info("Directory %s not in project to copy" % copyDir)
                continue
            logger.info("Copying files from %s to all devices in %s environment..." %(copyDir, svn_env)
            rmsg = dpx.sendTreeToDpLocal(copyDir)
            if rmsg != 'OK':
                logger.warning(rmsg)

        # ZIP bundles
        # Step 1: send env's dpolicy if it has one
        dpolicyName = ""

        dpolicySvnPath = '%s/%s/DeploymentPolicy' %(svnPath, svn_env)
        if not os.path.exists(dpolicySvnPath):
            logger.info("No Deployment policy directory exists for the environment selected")
        else:
            os.chdir(dpolicySvnPath)

            for fname in os.listdir('.'):
                # check to see if it contains local files
                z = zipfile.ZipFile(file)
                for fname in z.namelist():
                    if fname.startswith('local/'):
                        logger.warning('Deployment policy %s contains local file %s' %(file, fname))
                # strip zip extension for name of this deploy policy -- we will use it later
                dpolicyName = fileName.split(".")[0]
                # send this zip bundle to Datapower
                rmsg = dpx.doImport(fname)
                if rmsg != 'OK':
                    logger.warning(rmsg)
                    sys.exit(99)

    #deploy config zip files to DataPower
        configSvnPath = svnPath + "/Config"
        if not os.path.exists(configSvnPath):
            logger.info("No Config directory for the current project")
        else:
            os.chdir(configSvnPath)

            for file in os.listdir('.'):
                # note we use the dpolicy we just sent
                rmsg = dpx.doImport(file, dpolicyName)
                if rmsg != 'OK':
                    logger.warning(rmsg)
                    sys.exit(99)

        #persist the changes to datapower
        rmsg = dpx.saveConfig()
        if rmsg != 'OK':
            logger.warning(rmsg)
            sys.exit(99)

    #call cleanup function and sys.exit script
    cleanup()
    sys.exit(0)

