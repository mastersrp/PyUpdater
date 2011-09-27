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
# -- System libs --
import sys, os, tarfile, hashlib
import json, subprocess
# Checking for the 'core' dir.
# This is used for all custom python libs
if( os.access(os.path.abspath(os.curdir)+os.sep+"core", os.R_OK) == True):
    sys.path.append(os.path.abspath(os.curdir)+os.sep+"core")
else:
    print( "'"+os.path.abspath(os.curdir)+os.sep+"core' wasn't found!")
    print( "* RUNNING EMERGENCY UPDATE !!" )
    import urllib.request
    class bcolors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'
    MIRROR = "http://dl.dropbox.com/u/5579836/REPO/PAK/" # This is a fallback mirror
    WORKDIR = "."
    print( ">>> Downloading 'PyUpdater.tar.bz2'...", end="" )
    urllib.request.urlretrieve( MIRROR+"PyUpdater.tar.bz2", "PyUpdater.tar.bz2" )
    print( "Done!" )
    print( ">>> Extracting 'PyUpdater.tar.bz2'...", end="" )
    tarfile.open("PyUpdater.tar.bz2").extractall()
    print( "Done!" )
    print( ">>> Removing 'PyUpdater.tar.bz2'...", end="" )
    os.remove( "PyUpdater.tar.bz2" )
    print( "Done!" )
    print( "Emergency update completed." )
    sys.path.append( os.path.abspath( os.curdir )+os.sep+"core")
if( os.path.exists( "packages.settings.json" ) == False or os.path.isfile( "packages.settings.json" ) == False ):
    print( "* No settings file found, creating one." )
    MIRROR = ["http://dl.dropbox.com/u/5579836/REPO/"] # Default fallback
    WORKDIR = "root"
    BACKUPDIR = "backups"
    OUTFILE = { "mirror":MIRROR, "workdir":WORKDIR, "backupdir":BACKUPDIR }
    OUTFILE = json.dumps( OUTFILE, indent=4 )
    print( "-"*10+" Content of 'packages.settings.json' "+"-"*10 )
    print( str(OUTFILE) )
    print( "-"*57 )
    open( "packages.settings.json", "w").write( OUTFILE )
# -- Custom libs --
import varCheck
import settings
import packages
import compile
import clean
import get
from colors import bcolors

def sync( MIRROR ):
    if( os.path.exists( "packages.checksum" ) == False ):
        os.makedirs( "packages.checksum" )
    print( ">>> Updating packages list..." )
    get.download( True, MIRROR+"packages.rules.tar.bz2.checksum", "packages.checksum"+os.sep+"packages.rules.tar.bz2.checksum" )
    if( os.path.exists( "packages.rules" ) == False ):
        os.makedirs("packages.rules")
    get.download( True, MIRROR+"packages.rules.tar.bz2", "packages.rules.tar.bz2" )
    TARFILE = tarfile.open( "packages.rules.tar.bz2" )
    print( ">>> Extracting rules...", end="" )
    TARFILE.extractall( "packages.rules" )
    TARFILE.close()
    del TARFILE
    print( "Done!" )          
    print( ">>> Removing \"packages.rules.tar.bz2\"...", end="" )
    os.remove( "packages.rules.tar.bz2" )
    print( "Done!" )

def update(PAK, MIRROR, WORKDIR):
    """
    Update package 'PAK' in packages.rules.
    MIRROR is either a http or a ftp URL
    WORKDIR is the root directory to install everything to.
    """
    if( MIRROR.endswith("/PAK/") == False ):
        MIRROR = MIRROR+"/PAK/"
    elif( MIRROR.endswith("PAK/") == False):
        MIRROR = MIRROR+"PAK/"
    # --- Below this line: SETUP VARIABLES ---
    if(PAK.endswith(".json")==False):
        if(os.path.isdir("packages.rules"+os.sep+PAK)):
            return
        PAK=PAK+".json"  # Easier JSON reading in the future.
                            # Works better than constantly appending '.json' to PAK.
    TARFILE=packages.getTarfile(PAK)
    if (TARFILE == None):
        print( PAK+" doesn't point to a file. What do?")
        sys.exit(1)
    if (TARFILE.startswith("http://") == True or TARFILE.startswith("ftp://") == True or TARFILE.startswith("https://") == True):
        FILE = TARFILE.split("/")[-1]
        MIRROR=TARFILE[0:-len(FILE)]
        TARFILE=TARFILE[-len(FILE):]
    if( TARFILE.endswith("bz2") == True):
        TARTYPE = "bz2"
    elif( TARFILE.endswith( "gz") == True):
        TARTYPE = "gz"
    else:
        print( bcolors.RED+"* WARNING"+bcolors.ENDC+": Tar file isn't bz2 or gzip")
    NAME = json.loads( open( "packages.rules"+os.sep+PAK).read() ).get("name")
    if (NAME == None):
        NAME=TARFILE[:-8]
    INSTDIR=packages.getInstdir(PAK)
    if( os.path.exists(WORKDIR) == False):
        os.mkdir(WORKDIR)
    DEPENDS = []
    DEPENDS=packages.getDepend(PAK)
    bcolors.YES = bcolors.GREEN+"Y"+bcolors.ENDC
    bcolors.NO = bcolors.RED+"n"+bcolors.ENDC
    if( DEPENDS != None):
        for DEPEND in DEPENDS:
            DEPENDTAR = packages.getTarfile(DEPEND+".json")
            if( os.path.exists( "packages.checksum"+os.sep+DEPENDTAR+".checksum" ) == True):
                DEPENDS.remove(DEPEND)
                continue
        if( DEPENDS != [] ):
            print( PAK+" depends on" )
            print( DEPENDS )
            print( "Install above dependencies?"+" ["+bcolors.YES+"/"+bcolors.NO+"]")
            IN = input()
            if( IN.endswith("\r")==True ):
                IN = IN[:-1]
            while( IN.lower() != "y" or IN.lower() != "yes"):
                if( IN.lower() == "n" or IN.lower() == "no"):
                    return
                if( IN.lower() == "y" or IN.lower() == "yes"):
                    break
                if( IN.lower() == "" ):
                    break
                print( "Sorry, answer not recognized '"+IN+"'" )
                IN = input()
                if( IN.endswith("\r")==True ):
                    IN = IN[:-1]
            for DEPEND in DEPENDS:
                RETCODE = update(DEPEND, MIRROR, WORKDIR)
                if( RETCODE == 1):
                    sys.exit(1)
                DEPENDS.remove(DEPEND)
    INSTALLSCRIPT = packages.getInstallScript(PAK) # If this isn't needed, we won't use it.

    # --- Below this line: PRINT PACKAGE CRITICAL INFO ---
    print( bcolors.GREEN+"*"+bcolors.ENDC+" "+"Name"+": "+NAME)
    print( bcolors.GREEN+"*"+bcolors.ENDC+" "+"Package JSON"+": "+PAK)
    print( bcolors.GREEN+"*"+bcolors.ENDC+" "+"Package file"+": "+TARFILE)

    # --- Below this line: ACTUALLY UPDATE PACKAGE 'PAK' ---
    print(">>> Fetching checksum"+" '"+TARFILE+".checksum'")
    get.download(args.VERBOSE,MIRROR+TARFILE+".checksum", WORKDIR+TARFILE+".checksum")
    m = open(WORKDIR+TARFILE+".checksum", 'r').read()
    print( bcolors.GREEN+"*"+bcolors.ENDC+" SHA-1: "+m.split("\n")[0] )
    if ( os.path.exists("packages.checksum"+os.sep+TARFILE+".checksum") == False ):
        if ( os.access("packages.checksum"+os.sep, os.F_OK) == False):
            os.mkdir("packages.checksum")
        print( ">>> Downloading"+" '"+TARFILE+"' -> '"+WORKDIR+TARFILE+"'")
        get.download( True, MIRROR+TARFILE, WORKDIR+TARFILE )
        m = hashlib.sha1(open(WORKDIR+TARFILE, "rb").read()).hexdigest()
    else:
        mm = open("packages.checksum"+os.sep+TARFILE+".checksum", "r").read()
        if ( m == mm ):
            print( "Project is up-to-date!")
            clean.rm(WORKDIR+TARFILE+".checksum")
            return
        else:
            print( ">>> Downloading"+" '"+TARFILE+"' -> '"+WORKDIR+TARFILE+"'")
            get.download( True, MIRROR+TARFILE, WORKDIR+TARFILE )
            m = hashlib.sha1(open(WORKDIR+TARFILE, "rb").read()).hexdigest()
            
    # --- Below this line: EXTRACT UPDATE PACKAGE 'PAK' ---
    FILE = tarfile.open(WORKDIR+TARFILE, 'r')
    if( args.VERBOSE == False ):
        print( ">>> Extracting '"+TARFILE+"' -> '"+WORKDIR+INSTDIR+"'")
        FILE.extractall(WORKDIR+INSTDIR)
    else:
        print( ">>> Extracting '"+FILE.name.split(os.sep)[-1]+"'" )
        MEMBERS=FILE.getmembers()
        for MEMBS in MEMBERS:
            print( ">>> '"+WORKDIR+INSTDIR+MEMBS.name+"'")
            FILE.extract(MEMBS.name, WORKDIR+INSTDIR)
    FILE.close()
    del FILE
    clean.rm(WORKDIR+TARFILE)
    
    # --- Below this line: INSTALLSCRIPT ---
    CXX = compile.check(PAK, WORKDIR=WORKDIR)
    if( CXX != None):
        print( bcolors.GREEN+"*"+bcolors.ENDC+" CXX: "+CXX)
        CXX = compile.compile(PAK, CXX, WORKDIR)
    if( CXX != None and CXX != 0 ):
        print( bcolors.RED+"[ERROR]: Couldn't compile!" )
        print( ">>> Cleaning up and returning 1!"+bcolors.ENDC )
        # clean.rm( WORKDIR+INSTDIR ) -- NO U
        clean.rm( WORKDIR+TARFILE )
        clean.rm( WORKDIR+TARFILE+".checksum" )
        return 1
    del CXX

    # --- Below this line: sha1 hash generation ---
    mOut = open("packages.checksum"+os.sep+TARFILE+".checksum", "w")
    mOut.write(m)
    mOut.close()
    del m
    os.remove(WORKDIR+TARFILE+".checksum")

    # --- Below this line: Project is now installed, write to "packages.installed" ---
    if( os.path.isfile( "packages.installed" ) == False):
        PACKINST = []
    else:
        PACKINST = open( "packages.installed", "r" ).read().split("\n")
    while( PACKINST.count(PAK[:-5]) > 0 ):
        PACKINST.remove(PAK[:-5])
    while( PACKINST.count("\n") > 0 ):
        PACKINST.remove("\n")
    while( PACKINST.count("") > 0 ):
        PACKINST.remove("")
    PACKOUT = open( "packages.installed", "w" )
    for LINES in PACKINST:
        PACKOUT.write(LINES+"\n")
    PACKOUT.write(PAK[:-5]+"\n")
    PACKOUT.close()
    del PACKOUT

    # --- Below this line: REMOVE UNNEEDED FILES (IF THEY EXIST) ---
    CLEANUP = [WORKDIR+TARFILE, WORKDIR+TARFILE+".checksum"]
    for FILES in CLEANUP:
        if( os.path.exists(FILES) == False):
            continue
        clean.rm( FILES )
    del CLEANUP

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser( description='Update and build packages.' )
    parser.add_argument( "-v", "--verbose", action="store_true", dest="VERBOSE", default=False, help="Print ALL information!")
    parser.add_argument( "string", metavar="PAK", type=str, nargs="*" )
    parser.add_argument( "-S", "--sync", action="store_true", default=False, help="Syncronize package list first")
    args = parser.parse_args()
    
    MIRROR = settings.getMirror()
    if(MIRROR == None):
        sys.exit(1)
    MIRROR=MIRROR[0]
    WORKDIR = settings.getWorkdir()
    print("WORKDIR: "+WORKDIR)
    print("MIRROR: "+MIRROR)
    if( args.sync == True or os.path.exists("packages.rules") == False ):
        sync( MIRROR )
    if( len(sys.argv) < 2 ):
        sys.exit(0)
    for ARGS in args.string:
        if(ARGS.lower() == "all"):
            if( os.path.isfile( "packages.installed" ) == False):
                print( "No packages installed!" )
                continue
            else:
                PACKINST = open("packages.installed", "r").read().split("\n")
                print( PACKINST[:-1] )
                for LINES in PACKINST:
                    RETCODE = update(LINES, MIRROR, WORKDIR)
                    if( RETCODE == 1):
                        sys.exit(1)
                del PACKINST
                continue
        if ( os.access("packages.rules"+os.sep+ARGS+".json", os.R_OK) == True):
            RETCODE = update(ARGS, MIRROR, WORKDIR)
            if( RETCODE == 1):
                sys.exit(1)
        elif( os.path.isdir("packages.rules"+os.sep+ARGS) == True):
            LIST = os.listdir("packages.rules"+os.sep+ARGS)
            for FILES in LIST:
                if( FILES.endswith(".json") == True):
                    RETCODE = update(FILES, MIRROR, WORKDIR)
                    if( RETCODE == 1):
                        sys.exit(1)
        elif( ARGS != sys.argv[0]):
            print( "Package '"+ARGS+"' doesn't exist!")
            sys.exit(1)
