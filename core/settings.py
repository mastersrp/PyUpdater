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

def getMirror():
    JSON = json.loads(open("packages.settings.json", "r").read())
    mirrors = JSON.get("mirror")
    if( len(mirrors) >= 1):
        return mirrors
    else:
        print( "ERROR: NO mirrors found!" )
        return None

def getWorkdir():
    JSON = json.loads( open("packages.settings.json", "r").read() )
    workdir = JSON.get("workdir")
    if( workdir == None):
        print( "ERROR: NO Working Directory!" )
        return None
    if(workdir.endswith(os.sep) == False):
        workdir = workdir+os.sep
    return workdir

def getBackupdir():
    JSON = json.loads( open("packages.settings.json", "r").read() )
    backupdir = JSON.get("backupdir")
    if( backupdir == None):
        print( "ERROR: NO Backup Directory!" )
        return None
    if( backupdir.endswith(os.sep) == False):
        backupdir = backupdir+os.sep
    return backupdir
