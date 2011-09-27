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
import os
import json
# custom libs
import varCheck

def getTarfile(PAK):
    """
    Parses "packages.rules"+os.sep+PAK, must be a JSON file.

    Returns the 'tarfile' tag text.
    """
    JSON = json.loads( open("packages.rules"+os.sep+PAK).read() )
    TARFILE=JSON.get("tarfile")
    if (TARFILE == None):
        return None
    if (TARFILE.startswith("http://") == True or TARFILE.startswith("ftp://") == True or TARFILE.startswith("https://") == True):
        FILE="%s" % (
            TARFILE.split("/")[-1]
        )
        TARFILE=FILE
        FILE=None
    if ( TARFILE.startswith("git://") == True):
        print( "Sorry, GIT is currently NOT supported!" )
        sys.exit(1)
    return TARFILE
    
def getInstdir(PAK):
    """
    Parses "packages.rules"+os.sep+PAK, must be a JSON file.

    Returns the 'instdir' tag text.
    """
    if( PAK.endswith(".json") == False):
        PAK = PAK+".json"
    JSON = json.loads( open("packages.rules"+os.sep+PAK).read() )
    INSTDIR = JSON.get("instdir")
    if ( INSTDIR == None ):
        INSTDIR = getTarfile(PAK)[:-8]
    if( INSTDIR.endswith(os.sep) == False):
        INSTDIR=INSTDIR+os.sep
    INSTDIR=varCheck.do(INSTDIR)
    return INSTDIR
    
def getInstallScript(PAK):
    """
    Parses "packages.rules"+os.sep+PAK, must be a JSON file.
    
    Returns the 'installscript' tag.
    """
    if( PAK.endswith(".json") == False):
        PAK = PAK+".json"
    JSON = json.loads( open("packages.rules"+os.sep+PAK).read() )
    INSTALLSCRIPT = JSON.get("installscript")
    return INSTALLSCRIPT
    
def getDepend(PAK):
    """
    Parses "packages.rules"+os.sep+PAK, must be a JSON file.
    
    Returns the 'depend' tag, with all dependencies
    """
    if( PAK.endswith(".json") == False):
        PAK=PAK+".json"
    JSON = json.loads( open("packages.rules"+os.sep+PAK).read() )
    DEPENDS = JSON.get("depend")
    if( DEPENDS != None):
        for DEPEND in DEPENDS:
            DEPENDS.remove(DEPEND)
            DEPEND = varCheck.do(DEPEND)
            DEPENDS.append(DEPEND)
    return DEPENDS
