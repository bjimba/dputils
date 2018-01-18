#!/usr/bin/env python

from __future__ import print_function
import base64
import logging
import os
import sys
import urllib2

# if python < 2.5, get ElementTree.py from effbot.org and do this:
#import ElementTree as ET
# for newer pythons, it's standard
import xml.etree.ElementTree as ET

# print to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# constants not part of object
ns = {'dp': 'http://www.datapower.com/schemas/management'}

class dpxml:
    # if dryrun true, we don't send XML to DataPower
    dryrun = False
    # if verbose true, req and resp XML echo to stdout
    verbose = False
    # these can be overridden if the DP box is set oddly
    port = '5550'
    uri = '/service/mgmt/current'

    def __init__(self, host='', domain='', creds=''):
        self.host = host
        self.domain = domain
        self.creds = creds

    # common to all - xml in, xml out
    def callSoma(self, reqXml):
        # TODO - check first if self.creds is non-empty
        somaUrl = 'https://' + self.host + ':' + self.port + self.uri
        if self.verbose:
            eprint("dpxml: callSoma: somaUrl=" + somaUrl)
            eprint("dpxml: callSoma: reqXml=" + reqXml)
        if self.dryrun:
            return '<dryrun xmlns:dp="' + ns['dp'] + '"><dp:result>OK, dry run</dp:result></dryrun>'
        req = urllib2.Request(url=somaUrl, data=reqXml)
        req.add_header('Authorization', 'Basic %s' % base64.encodestring(self.creds))
        respXml = urllib2.urlopen(req).read()
        if self.verbose:
            eprint("dpxml: callSoma: respXml=" + respXml)
        return respXml


    # and now, the useful functions

    # for normal use, create an object, configure it, and call the useful functions

    #   dpx = dpxml.dpxml()
    #   dpx.host = '10.0.0.42'
    #   dpx.domain = 'my_dp_domain'
    #   dpx.creds = 'jprussell:password00'  # I don't really recommend this password

    # alternatively, you can create and configure with args:

#   dpx = dpxml.dpxml('10.0.0.42', 'my_dp_domain', 'jprussell:password00')

    # now, let's do something with it

    #   rmsg = dpx.createDir('local:///newdir')
    #   if rmsg = 'OK':
    #       eprint("Good")
    #   else:
    #       eprint("Bad: " + rmsg)


    # createDir: create directory on Datapower
    #   returns OK even if directory already exists
    def createDir(self, dpDir):
        if self.verbose:
            eprint("dpxml: setFile: ENTRY")
        reqXml = createXmlFromTemplate(reqCreateDir,
            {   'dir': dpDir,
                'domain': self.domain })
        respXml = self.callSoma(reqXml)
        # this returns dp:result - use common parser
        return parseDpResult(respXml)

    # doBackup: save whole domain to a backup ZIP-format file
    def doBackup(self, fspecZip):
        if self.verbose:
            eprint("dpxml: doBackup: ENTRY")
        reqXml = createXmlFromTemplate(reqDoBackup,
            {   'domain': self.domain })
        respXml = self.callSoma(reqXml)
        # special case parsing - dp:file
        respRoot = ET.fromstring(respXml)
        fileNode = respRoot.find('.//dp:file', ns)
        if fileNode is None:
            resultText = 'BACKUP FAILED: host=' + self.host + ', domain=' + self.domain
        else:
            b64 = fileNode.text
            # TODO - set rc on file errors
            f = open(fspecZip, 'wb')
            f.write(base64.b64decode(b64))
            f.close()
            resultText = 'OK'
        return resultText

    # doImportXcfg: import configuration xml file, with optional deployment policy
    def doImportXcfg(self, fspec, deployPolicy=''):
        if self.verbose:
            eprint("dpxml: doImportXcfg: ENTRY")
        # TODO - set rc on file errors
        f = open(fspec, 'rb')
        fData = f.read()
        f.close()
        fB64 = base64.b64encode(fData)
        reqXml = createXmlFromTemplate(reqDoImportXcfg,
            {   'b64File': base64.b64encode(fData),
                'deploymentPolicy': deployPolicy,
                'domain': self.domain })
        respXml = self.callSoma(reqXml)
        # special case parsing - dp:import
        respRoot = ET.fromstring(respXml)
        importNode = respRoot.find('.//dp:import', ns)
        if importNode is None:
            resultText = 'IMPORT FAILED: file=' + fspec + ', host=' + self.host + ', domain=' + self.domain
        else:
            failNodes = importNode.findall(".//*[@status='FAIL']")
            errorNodes = importNode.findall(".//*[@status='ERROR']")
            if len(failNodes) > 0 or len(errorNodes) > 0:
                resultText = 'IMPORT WARNING: file=' + fspec + ', host=' + self.host + ', domain=' + self.domain
                resultText += ' -- ERRORS=' + str(len(errorNodes)) + ', FAILS=' + str(len(failNodes))
            else:
                resultText = 'OK'
        return resultText

    # doImportZip: import configuration zip file, with optional deployment policy
    def doImportZip(self, fspec, deployPolicy=''):
        if self.verbose:
            eprint("dpxml: doImportZip: ENTRY")
        # TODO - set rc on file errors
        f = open(fspec, 'rb')
        fData = f.read()
        f.close()
        fB64 = base64.b64encode(fData)
        reqXml = createXmlFromTemplate(reqDoImportZip,
            {   'b64File': base64.b64encode(fData),
                'deploymentPolicy': deployPolicy,
                'domain': self.domain })
        respXml = self.callSoma(reqXml)
        # special case parsing - dp:import
        respRoot = ET.fromstring(respXml)
        importNode = respRoot.find('.//dp:import', ns)
        if importNode is None:
            resultText = 'IMPORT FAILED: file=' + fspec + ', host=' + self.host + ', domain=' + self.domain
        else:
            failNodes = importNode.findall(".//*[@status='FAIL']")
            errorNodes = importNode.findall(".//*[@status='ERROR']")
            if len(failNodes) > 0 or len(errorNodes) > 0:
                resultText = 'IMPORT WARNING: file=' + fspec + ', host=' + self.host + ', domain=' + self.domain
                resultText += ' -- ERRORS=' + str(len(errorNodes)) + ', FAILS=' + str(len(failNodes))
            else:
                resultText = 'OK'
        return resultText

    # getStatusFirmware
    def getStatusFirmware(self):
        if self.verbose:
            eprint("dpxml: getStatusFirmware: ENTRY")
        reqXml = createXmlFromTemplate(reqGetStatusFirmware,
            { 'domain': self.domain })
        respXml = self.callSoma(reqXml)
        #return 'ok'
        return respXml

    # saveConfig: tell DataPower to persist the running config
    def saveConfig(self):
        if self.verbose:
            eprint("dpxml: saveConfig: ENTRY")
        reqXml = createXmlFromTemplate(reqSaveConfig,
            { 'domain': self.domain })
        respXml = self.callSoma(reqXml)
        # this returns dp:result - use common parser
        return parseDpResult(respXml)

    # setFile: upload a file to DataPower
    def setFile(self, fspec, dpPath):
        if self.verbose:
            eprint("dpxml: setFile: ENTRY")
        # TODO - set rc on file errors
        f = open(fspec, 'rb')
        fdata = f.read()
        reqXml = createXmlFromTemplate(reqSetFile,
            {   'filename': dpPath,
                'b64file': base64.b64encode(fdata),
                'domain': self.domain })
        respXml = self.callSoma(reqXml)
        # this returns dp:result - use common parser
        return parseDpResult(respXml)

    def sendTreeToDpLocal(self, path):

        if self.verbose:
            eprint("dpxml: sendTree: path=", path)

        # counts to return
        ct_dir = 0
        ct_file = 0

        # send tree at 'path' to Datapower local:///
        savewd = os.getcwd()
        os.chdir(path)

        for subdir, dirs, files in os.walk('.'):

            if self.verbose:
                eprint("dpxml: sendTree: subdir=", subdir)
                eprint("dirs: ", dirs)
                eprint("files: ", files)
                eprint("function level path: ", path)

            # we're walking down tree, starting at cwd
            # at each step:
            #   assume subdir is already on DP (since we start at '.', and create [ dirs ])
            #   create any dirs in [ dirs ]
            #   send any file in [ files ]

            subdir = subdir.replace('\\','/')

            # what we expect is "root" subdir of '.', followed by
            # subdirs like './xxx', './xxx/yyy'

            if subdir == '.':
                currdir = ''
            elif '.' == subdir[0]:
                currdir = subdir[1:]
            else:
                # this shouldn't happen
                currdir = subdir

            for dir in dirs:
                localdir = 'local:///' + path + currdir + '/' + dir
                if self.verbose:
                    eprint("localdir: " + localdir)
                eprint("createDir localdir=" + localdir)
                rmsg = self.createDir(localdir)
                # we should make use of rmsg
                ct_dir += 1

            #logger.info("Copying all files from %s to dp local:///%s" %(
            #    subdir, currdir))

            for file in files:
                if currdir == '':
                    fullpath = file
                else:
                    fullpath = currdir[1:] + '/' + file
                #fullpath = os.path.join(currdir, file)
                if self.verbose:
                    eprint("fullpath: " + fullpath)
                dpPath = 'local:///' + path + currdir + '/' + file
                if self.verbose:
                    eprint("dppath: " + dpPath)
                eprint("setFile fullpath=" + fullpath + " dpPath=" + dpPath)
                rmsg = self.setFile(fullpath, dpPath)
                #if rmsg != 'OK':
                #    #logger.warning('DP Set File error: %s' % rmsg)
                #    return rmsg
                ct_file += 1

        os.chdir(savewd)
        #return rmsg
        return str(ct_dir) + " dirs, " + str(ct_file) + " files"

# these are not part of class object

# many SOMA calls return dp:result - common parser here
#   response XML in, text out
#   success is 'OK'
def parseDpResult(respXml):
    respRoot = ET.fromstring(respXml)
    resultNode = respRoot.find('.//dp:result', ns)
    # errors have no text at this level, look for error further down
    errLogNode = resultNode.find('error-log/log-event')
    if errLogNode is not None:
        resultText = errLogNode.text
    else:
        # success will return 'OK', usually surrounded by copious whitespace
        resultText = resultNode.text.strip()
    return resultText


# the actual SOMA SOAPs live here, in templates

def createXmlFromTemplate(template, paramDict):
    xml = template
    for k, v in paramDict.items():
        xml = xml.replace('%' + k + '%', v)
    return xml

# request templates

reqCreateDir = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
       <dp:request domain="%domain%" xmlns:dp="http://www.datapower.com/schemas/management">
          <dp:do-action>
             <CreateDir>
                <Dir>%dir%</Dir>
             </CreateDir>
          </dp:do-action>
       </dp:request>
    </env:Body>
</env:Envelope>
"""
reqDoBackup = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <dp:request xmlns:dp="http://www.datapower.com/schemas/management">
            <dp:do-backup format="ZIP">
                <dp:domain name="%domain%"/>
            </dp:do-backup>
        </dp:request>
    </env:Body>
</env:Envelope>
"""
reqDoImportXcfg = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <dp:request xmlns:dp="http://www.datapower.com/schemas/management"
            domain="%domain%">
            <dp:do-import source-type="XML" overwrite-objects="true"
                overwrite-files="false" deployment-policy="%deploymentPolicy%">
                <dp:input-file>%b64File%</dp:input-file>
            </dp:do-import>
        </dp:request>
    </env:Body>
</env:Envelope>
"""
reqDoImportZip = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <dp:request xmlns:dp="http://www.datapower.com/schemas/management"
            domain="%domain%">
            <dp:do-import source-type="ZIP" overwrite-objects="true"
                overwrite-files="true" deployment-policy="%deploymentPolicy%">
                <dp:input-file>%b64File%</dp:input-file>
            </dp:do-import>
        </dp:request>
    </env:Body>
</env:Envelope>
"""
reqGetStatusFirmware = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
<env:Body>
<dp:request xmlns:dp="http://www.datapower.com/schemas/management"
    domain="%dpdomain%">
<dp:get-status class="FirmwareVersion"/>
</dp:request>
</env:Body>
</env:Envelope>
"""
reqSaveConfig = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <dp:request xmlns:dp="http://www.datapower.com/schemas/management" domain="%domain%">     
           <dp:do-action>
              <SaveConfig/>
           </dp:do-action>
        </dp:request>
    </env:Body>
</env:Envelope>
"""
reqSetFile = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <dp:request xmlns:dp="http://www.datapower.com/schemas/management" domain="%domain%">
            <dp:set-file name="%filename%">%b64file%</dp:set-file>
        </dp:request>
    </env:Body>
</env:Envelope>
"""
reqXxx = """<?xml version="1.0" encoding="UTF-8"?>
"""

# not implemented yet

reqGetSamlArt = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <dp:request xmlns:dp="http://www.datapower.com/schemas/management" domain="%domain%">
            <dp:get-samlart user="%user%" password="%passwd%"/>
        </dp:request>
    </env:Body>
</env:Envelope>
"""

reqDoExport = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <dp:request xmlns:dp="http://www.datapower.com/schemas/management" domain="%domain%">
            <dp:do-export format="" all-files="" persisted="" deployment-policy="">
                <dp:user-comment>%comment%</dp:user-comment>
                <dp:object class="" name="" ref-objects="" ref-files="" include-debug=""/>
                <dp:deployment-policy/>
            </dp:do-export>
        </dp:request>
    </env:Body>
</env:Envelope>
"""
reqGetStatusFirmware = """<?xml version="1.0" encoding="UTF-8"?>
<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
    <env:Body>
        <dp:request xmlns:dp="http://www.datapower.com/schemas/management" domain="%domain%">
            <dp:get-status class="FirmwareVersion"/>
        </dp:request>
    </env:Body>
</env:Envelope>
"""
