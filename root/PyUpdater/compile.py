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
import sys, os, subprocess
import json
# Checking for the 'core' dir.
# This is used for all custom python libs
if( os.access(os.curdir+os.sep+"core", os.R_OK) == True):
    sys.path.append(os.curdir+os.sep+"core")
else:
    print( "'"+os.curdir+os.sep+"core' wasn't found!")
    sys.exit(1)
# -- Custom libs --
import find
import settings
import packages
from colors import *

def check( PAK, WORKDIR):
    if( PAK.endswith(".json") == False):
        PAK = PAK+".json"
    INSTDIR = packages.getInstdir(PAK)
    INSTALLSCRIPT = packages.getInstallScript(PAK)
    HOMEROOT=os.path.abspath(os.curdir)
    os.chdir(WORKDIR+INSTDIR)
    if( INSTALLSCRIPT != None):
        os.chdir(HOMEROOT)
        return os.path.abspath(WORKDIR+INSTDIR+INSTALLSCRIPT)
    if(os.access("Makefile", os.R_OK) == True):
        CXX="make"
        os.chdir(HOMEROOT)
        return CXX
    elif( os.access("CMakeLists.txt", os.R_OK) == True):
        CXX="cmake && make"
        GEN="\"Unix Makefiles\""
        if( os.name.lower() == "msys" ):
            GEN="\"MSYS Makefiles\""
        os.chdir(HOMEROOT)
        return CXX+" -G "+GEN
    elif( os.access("configure", os.X_OK) == True):
        CXX="configure && make"
        os.chdir(HOMEROOT)
        return CXX+" --prefix=/usr/bin"
    else:
        os.chdir(HOMEROOT)
        return None


def compile(PAK, CXX, WORKDIR):
    """
    'CXX' is the full path to the executable compiler.
    """
    if( PAK.endswith(".json") == False):
        PAK = PAK+".json"
    INSTDIR = packages.getInstdir(PAK)
    HOMEROOT=os.path.abspath(os.curdir)
    if( CXX != None ):
        HOMEROOT=os.path.abspath(os.curdir)
        print( bcolors.YELLOW+"cd: "+bcolors.ENDC+" Entering '"+WORKDIR+INSTDIR+"'")
        os.chdir(WORKDIR+INSTDIR)
        RETCODE = subprocess.call(CXX, shell=True)
        print( bcolors.YELLOW+"cd: "+bcolors.ENDC+" Leaving '"+WORKDIR+INSTDIR+"'")
        os.chdir(HOMEROOT)
        return RETCODE
if __name__ == "__main__":
    if(len(sys.argv)==1):
        # Display help
        sys.exit(1)
    WORKDIR = settings.getWorkdir()
    for ARGS in sys.argv[1:]:
        if(os.access("packages.rules"+os.sep+ARGS+".json", os.R_OK) == True):
            INSTDIR = packages.getInstdir(ARGS)
            if( os.access(WORKDIR+INSTDIR, os.W_OK) == False):
                    if( os.access(WORKDIR+INSTDIR, os.F_OK) == False):
                        print( "Trying to update...")
                        MIRROR = settings.getMirror()
                        if( MIRROR == None):
                            sys.exit(1)
                        MIRROR=MIRROR[0]
                        from update import *
                        if ( os.access("packages.rules"+os.sep+ARGS+".json", os.R_OK) == True):
                            update(ARGS, MIRROR, WORKDIR)
                        elif( os.path.isdir("packages.rules"+os.sep+ARGS) == True):
                            LIST = os.listdir("packages.rules"+os.sep+ARGS)
                            for FILES in LIST:
                                update(FILES, MIRROR, WORKDIR)
                        elif( ARGS != sys.argv[0]):
                            print( "Package '"+ARGS+"' doesn't exist!")
                            sys.exit(1)
                    else:
                        print( "Cannot write to '"+INSTDIR+"' !")
                        sys.exit(1)
            else:
                CXX = check(ARGS, WORKDIR=WORKDIR)
                compile(ARGS, CXX=CXX, WORKDIR=WORKDIR)
