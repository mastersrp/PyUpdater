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
import os, sys, shutil, json
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

def rm(OBJ):
    if(os.access(OBJ, os.F_OK) == False):
        print("'"+OBJ+"' doesn't exist!")
        return
    if(os.access(OBJ, os.W_OK) == False):
        print("Cannot write/remove '"+OBJ+"'! Write-access = FALSE")
        return
    if(os.path.isdir(OBJ) == True):
        print("REM [R]'"+OBJ+"'")
        shutil.rmtree(OBJ)
        return
    else:
        print("REM '"+OBJ+"'")
        os.remove(OBJ)
        return

if __name__ == "__main__":
    WORKDIR = settings.getWorkdir()
    BACKUPDIR = settings.getBackupdir()
    for ARGS in sys.argv:
        if(ARGS == sys.argv[0]):
            continue
        if(os.access("packages.rules"+os.sep+ARGS+".json", os.R_OK) == True):
            INSTDIR=packages.getInstdir(ARGS+".json")
            TARFILE=packages.getTarfile(ARGS+".json")
            if(INSTDIR==None):
                INSTDIR=TARFILE[:-8]
            rm(WORKDIR+INSTDIR)
            rm("packages.checksum"+os.sep+TARFILE+".checksum")
            if( os.path.isfile("packages.installed") == True):
                PACK = open("packages.installed","r").read().split("\n")
                PACK.remove(ARGS)
                PACKOUT = open("packages.installed", "w")
                for LINES in PACK:
                    PACKOUT.write(LINES+"\n")
                PACKOUT.close()
                del PACK
                del PACKOUT
            continue
        if(ARGS.lower() == "all"):
            if( os.path.exists("packages.installed") == False):
                continue
            PACKINST = open("packages.installed", "r").read().split("\n")
            PACKINST.remove("")
            for LINES in PACKINST:
                INSTDIR = packages.getInstdir(LINES+".json")
                rm(WORKDIR+INSTDIR)
            del PACKINST
            rm("packages.installed")
            rm("packages.checksum")
            rm("core"+os.sep+"__pycache__")
            rm("__pycache__" )
            continue
        if(os.access(ARGS, os.W_OK) == True):
            rm(ARGS)
