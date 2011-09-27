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
import os, sys

def find(OBJ, TOLOWER=True, PATH=os.environ['PATH'].split(os.pathsep) ):
    PATHFOUND=False
    for PATHS in paths:
        if( os.access(PATHS, os.R_OK) == False):
            continue
        for DIRS in os.listdir( PATHS ):
            if(TOLOWER):
                DIRS=DIRS.lower()
                OBJ=OBJ.lower()
            else:
                DIRS=DIRS
                OBJ=OBJ
            if( DIRS.endswith(OBJ) == True):
                return PATHS+os.sep+OBJ
                PATHFOUND=True
                break
            else:
                continue
        if(PATHFOUND==True):
            break
        else:
            continue
    if( PATHFOUND==False):
        return None

if __name__=="__main__":
    for args in sys.argv[1:]:
        OUT=find(args)
        if(OUT != None):
            print(OUT)
