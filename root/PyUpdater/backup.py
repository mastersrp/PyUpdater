#!/usr/bin/env python3.2
#Copyright (C) 2011 by Steffen Rytter Postas
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE
import os, sys, tarfile, hashlib
import json
# Checking for the 'core' dir.
# This is used for all custom python libs
if( os.access(os.curdir+os.sep+"core", os.R_OK) == True):
    sys.path.append(os.curdir+os.sep+"core")
else:
    print( "'"+os.curdir+os.sep+"core' wasn't found!")
    sys.exit(1)
# -- Custom libs --
import varCheck
import settings
import packages
from colors import *

def backup(OBJ, WORKDIR, BACKUPDIR):
    """
    Backup OBJ from WORKDIR, to BACKUPDIR.
    The installation directory of OBJ will be read from OBJ+'.json'
    OBJ will be packaged in BACKUPDIR as NAME+'.tar.bz2'
    """
    if(os.access("packages.rules"+os.sep+OBJ+".json", os.R_OK) == True):
            INSTDIR = packages.getInstdir(OBJ+".json")
            BACKUPTAR = packages.getTarfile(OBJ+".json")
            if(BACKUPTAR.startswith("http://") == True):
                BACKUPTAR="%s" % (
                    BACKUPTAR.split("/")[-1]
                )
            if (INSTDIR == None):
                INSTDIR=WORKDIR+BACKUPTAR[:-8]
            else:
                INSTDIR=WORKDIR+INSTDIR
            INSTDIR=varCheck.do(INSTDIR)
            if (INSTDIR.endswith(os.sep) == False):
                INSTDIR=INSTDIR+os.sep
            if(os.access(BACKUPDIR, os.F_OK) == False):
                os.makedirs(BACKUPDIR)
            if(os.access(WORKDIR, os.F_OK) == False):
                print( bcolors.RED+"Workdir '"+WORKDIR+"' does NOT exist!"+bcolors.ENDC)
                sys.exit(1)
            if(os.access(INSTDIR, os.F_OK) == False):
                print( bcolors.RED+"Package '"+OBJ+"' is NOT installed."+bcolors.ENDC)
                return
            TARFILE=tarfile.open(BACKUPDIR+BACKUPTAR, "w:bz2")
            if(args.QUIET==False or None):
                print( bcolors.GREEN+"+"+bcolors.ENDC+"--"+OBJ+".json" )
            if( INSTDIR==(WORKDIR+"."+os.sep) ):
                print( "(WIP)")
                return
            else:
                HOME=os.path.abspath(os.curdir)
                os.chdir(INSTDIR)
                for FILES in os.listdir(os.curdir):
                    if((FILES+os.sep)==BACKUPDIR):
                        continue
                    elif((FILES+os.sep)==WORKDIR):
                        continue
                    if(args.QUIET==False or None):
                        print( bcolors.YELLOW+"|"+bcolors.ENDC+"-"+FILES)
                    TARFILE.add(FILES)
                os.chdir(HOME)
            TARFILE.close()
            del TARFILE
            m = hashlib.sha1(open(BACKUPDIR+BACKUPTAR, "rb").read()).hexdigest()
            if(args.NEW == True):
                if(os.access("packages.checksum"+os.sep+BACKUPTAR+".checksum", os.W_OK) == False):
                    print( "Please re-run this script with write-access to 'packages.checksum"+os.sep+"'.")
                    return
                mOut = open("packages.checksum"+os.sep+BACKUPTAR+".checksum", "w")
                mOut.write(m)
                mOut.close()
            mOut = open(BACKUPDIR+BACKUPTAR+".checksum", "w")
            mOut.write(m)
            mOut.close()
            del m
            del mOut

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Backup selected projects")
    parser.add_argument( "-n", "--new", action="store_true",dest="NEW", default=False, help="Overwrite installed checksums")
    parser.add_argument( "-q", "--quiet", action="store_true", dest="QUIET", default=False, help="Supress backup tree")
    parser.add_argument( "string", metavar="PAK", type=str, nargs="*" )
    args = parser.parse_args()
    
    WORKDIR = settings.getWorkdir()
    BACKUPDIR = settings.getBackupdir()
    if(args.QUIET==False or None):
        print( "BACKUPDIR: "+BACKUPDIR)
        print( "WORKDIR: "+WORKDIR)
    for ARGS in args.string:
        if(ARGS.lower()=="all"):
            if( os.path.exists("packages.installed") == False):
                continue
            LIST = open("packages.installed", "r").read().split("\n")
            for FILES in LIST:
                if(FILES.endswith(".json") == True):
                    FILES=FILES[:-5]
                backup(FILES, WORKDIR, BACKUPDIR)
            del LIST
        else:
            backup(ARGS, WORKDIR, BACKUPDIR)
