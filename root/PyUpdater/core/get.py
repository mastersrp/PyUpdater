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
"""
This Python 3.2 module is able to download files. That's it.
It's a very very basic version of wget on Linux, only crossplatform.
"""
import os, sys
import urllib.request

def cls( numlines=100 ):
    print( "\n"*numlines )

class C:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

if( os.name == "nt" ):
    C.HEADER = ''
    C.BLUE = ''
    C.GREEN = ''
    C.YELLOW = ''
    C.RED = ''
    C.ENDC = ''

def download( verbose, Url, OUTFILE ):
    try:
        UrlObj = urllib.request.urlopen( Url )
        length = UrlObj.getheader( "Content-Length" )
        OUT = open(OUTFILE, "wb" )
        if not length:
            length="?"
        if length!="?":
            length = int(length)
        bytesRead=0
        ASCIIBack = "\r"
        for LINE in UrlObj:
            bytesRead+=len(LINE)
            if (length!="?" and verbose==True):
                print( ASCIIBack+C.GREEN+OUTFILE+C.ENDC+": "+str( int(bytesRead/1024.0))+"/"+str(int(length/1024.0))+" kb ("+C.BLUE+str( int(100*bytesRead/length) )+C.ENDC+"%)", end="" )
            OUT.write(LINE)
        if( verbose==True):
            print( "" )
        OUT.close()
    except Exception:
        print( "Error downloading "+str(Url))
        print( C.RED+"DUNNO WAT WENT WRONG LOL FUK U"+C.ENDC)
        
        
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser( description="Download HTTP or FTP objects." )
    parser.add_argument( "url", metavar="URL", type=str, nargs=1 )
    parser.add_argument( "-v", "--verbose", action="store_true", default=False, help="Print ALL information!")
    parser.add_argument( "-o", "--out", metavar="filename", help="Filename to output.", )
    args = parser.parse_args()

    print( C.YELLOW+"[DEBUG]"+C.ENDC+" Verbose: "+str(args.verbose))
    if( args.out == None ):
        args.out = args.url[0].split("/")[-1]
    print( C.GREEN+"*"+C.ENDC+" URL: '"+args.url[0]+"'" )
    print( C.GREEN+"*"+C.ENDC+" Fetching '"+args.url[0].split("/")[-1]+"'" )
    print( C.GREEN+"*"+C.ENDC+" Filename: '"+args.out+"'" )
    print( C.YELLOW+"[DEBUG]"+C.ENDC+" Attempting download..." )
    download( args.verbose, args.url[0], args.out )
    print( "Done!" )
