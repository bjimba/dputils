#! /usr/bin/env python3

import click
import sys

from jimr import *

import dpxml
import dpxml_cfg as cfg

@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.option('--verbose / --no-verbose', default=False)
@click.argument('env')
@click.pass_context
def main(ctx, verbose, env):
    """This is main"""
    ctx.obj = {}
    ctx.obj['verbose'] = verbose

    #argparser = argparse.ArgumentParser()
    #argparser.add_argument('--verbose', action='store_true')
    #argparser.add_argument('env')
    #argparser.add_argument('op')
    #argparser.add_argument('params', nargs='*')
    #args = argparser.parse_args()

    if verbose:
        eprint("VERBOSE!")

    if not env in cfg.envs:
        eprint("No config for env " + env)
        sys.exit(1)

    thiscfg = cfg.envs[env]
    dp_host = thiscfg['host']
    dp_domain = thiscfg['domain']
    dp_creds = thiscfg['creds']
    dp_xmlport =thiscfg['xmlport']

    dpx = dpxml.dpxml(host=dp_host, domain=dp_domain, creds=dp_creds)
    #dpx.port = '5550'
    #dpx.port = '10550'
    dpx.port = dp_xmlport
    dpx.verbose = verbose

    ctx.obj['dpx'] = dpx
    # rmsg will be 'OK' on success, unless noted

@main.command()
@click.pass_context
def xyzzy(ctx):
    eprint("Nothing happens.")

@main.command()
@click.pass_context
@click.argument('dirspec')
def createdir(ctx, dirspec):
    eprint("createDir")
    eprint("dirspec=" + dirspec)
    dpx = ctx.obj['dpx']
    rmsg = dpx.createDir(dirspec)
    eprint("createDir response: ", rmsg)

@main.command()
@click.pass_context
@click.argument('zipspec')
def dobackup(ctx, zipspec):
    eprint("doBackup")
    dpx = ctx.obj['dpx']
    rmsg = dpx.doBackup(zipspec)
    eprint("DoBackup call response: ", rmsg)

@main.command()
@click.pass_context
@click.argument('xcfgspec')
@click.argument('deployPolicy')
def doimportxcfg(ctx, xcfgspec, deployPolicy):
    eprint("doImportXcfg")
    dpx = ctx.obj['dpx']
    if deployPolicy == 'NONE':
        deployPolicy = ''
    rmsg = dpx.doImportXcfg(xcfgspec, deployPolicy=deployPolicy)
    eprint("DoImportXcfg response: ", rmsg)

@main.command()
@click.pass_context
@click.argument('zipspec')
@click.argument('deployPolicy')
def doimportzip(ctx, zipspec, deployPolicy):
    eprint("doImportZip")
    dpx = ctx.obj['dpx']
    if deployPolicy == 'NONE':
        deployPolicy = ''
    rmsg = dpx.doImportZip(zipspec, deployPolicy=deployPolicy)
    eprint("DoImportZip response: ", rmsg)

@main.command()
@click.pass_context
def getstatusfirmware(ctx):
    eprint('getStatusFirmware')
    dpx = ctx.obj['dpx']
    rmsg = dpx.getStatusFirmware()
    # return the XML
    eprint(rmsg)

@main.command()
@click.pass_context
def saveconfig(ctx):
    # persist running config
    eprint('saveConfig')
    dpx = ctx.obj['dpx']
    rmsg = dpx.saveConfig()
    eprint("saveConfig response: ", rmsg)

@main.command()
@click.pass_context
@click.argument('fspec')
@click.argument('dstpath')
def setfile(ctx, fspec, dstpath):
    eprint('setFile')
    dpx = ctx.obj['dpx']
    rmsg = dpx.setFile(fspec, dstpath)
    eprint("setFile response: ", rmsg)

@main.command()
@click.pass_context
@click.argument('treepath')
def sendtree(ctx, treepath):
    # only one arg, tree path
    # dest is DP local:///
    # so, to populate ICET/Common:
    #   cd local
    #   sendtree ICET/Common
    eprint('sendTree')
    dpx = ctx.obj['dpx']
    rmsg = dpx.sendTreeToDpLocal(treepath)
    eprint("sendTree response: ", rmsg)


if __name__ == "__main__":
    main()
