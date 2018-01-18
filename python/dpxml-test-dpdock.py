from __future__ import print_function
import argparse
import sys

import dpxml

# print to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

dp_host = '10.124.30.30'
dp_domain = 'DBPL'
dp_creds = 'jimr:altcare'

dpx = dpxml.dpxml(host=dp_host, domain=dp_domain, creds=dp_creds)
dpx.port = '5550'
#dpx.port = '10550'
dpx.verbose = True

argparser = argparse.ArgumentParser()
argparser.add_argument('--verbose', action='store_true')
argparser.add_argument('op')
argparser.add_argument('params', nargs='*')
args = argparser.parse_args()

if args.verbose:
    eprint("VERBOSE!")

# rmsg will be 'OK' on success, unless noted

if args.op == 'xyzzy':
    eprint("Nothing happens.")

elif args.op.lower() == 'createdir':
    eprint("createDir")
    dirspec = args.params[0]
    eprint("dirspec=" + dirspec)
    rmsg = dpx.createDir(dirspec)
    eprint("createDir response: ", rmsg)

elif args.op.lower() == 'dobackup':
    eprint("doBackup")
    zipspec = args.params[0]
    rmsg = dpx.doBackup(zipspec)
    eprint("DoBackup call response: ", rmsg)

elif args.op.lower() == 'doimportxcfg':
    eprint("doImportXcfg")
    xcfgspec = args.params[0]
    deployPolicy = args.params[1]
    if deployPolicy == 'NONE':
        deployPolicy = ''
    rmsg = dpx.doImportXcfg(xcfgspec, deployPolicy=deployPolicy)
    eprint("DoImportXcfg response: ", rmsg)

elif args.op.lower() == 'doimportzip':
    eprint("doImportZip")
    zipspec = args.params[0]
    deployPolicy = ''
    if len(arg.params) > 1:
        deployPolicy = args.params[1]
    rmsg = dpx.doImportZip(zipspec, deployPolicy=deployPolicy)
    eprint("DoImportZip response: ", rmsg)

elif args.op.lower() == 'getstatusfirmware':
    eprint('getStatusFirmware')
    rmsg = dpx.getStatusFirmware()
    # return the XML
    eprint(rmsg)

elif args.op.lower() == 'saveconfig':
    # persist running config
    eprint('saveConfig')
    rmsg = dpx.saveConfig()
    eprint("saveConfig response: ", rmsg)

elif args.op.lower() == 'setfile':
    eprint('setFile')
    fspec = args.params[0]
    dstpath = args.params[1]
    rmsg = dpx.setFile(fspec, dstpath)
    eprint("setFile response: ", rmsg)

elif args.op.lower() == 'sendtree':
    # only one arg, tree path
    # dest is DP local:///
    # so, to populate ICET/Common:
    #   cd local
    #   sendtree ICET/Common
    eprint('sendTree')
    treepath = args.params[0]
    rmsg = dpx.sendTreeToDpLocal(treepath)
    eprint("sendTree response: ", rmsg)

else:
    eprint("Undefined op, try one of:")
    eprint("createDir local:///mydir")
    eprint("doBackup backfile.zip")
    eprint("doImportXcfg my.xcfg")
    eprint("dpImportZip my.zip")
    eprint("getStatusFirmware")
    eprint("saveConfig")
    eprint("setFile myfile.xxx local://mydir")
    eprint("sendTree path/to/send/to/local")



