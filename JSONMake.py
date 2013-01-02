#! /usr/bin/python2
'''
Python script to parse JSON makefiles. I'll add good doc strings later

@author: Sam Agnew
'''
import sys
import json
import subprocess
import os
import functions
import JSONMaker

try:
    with functions.openIgnoreCase('JSONMakefile') as f:
        makeFile = json.load(f)
except EnvironmentError:
    print >> sys.stderr, "JSON MakeFile not found!"
    sys.exit()
except IOError:
    print >> sys.stderr, "Error! No JSONMakefile in this directory!"
    sys.exit()
    
builder = JSONMaker.JSONMaker(makeFile)

try:
    if len(sys.argv) == 2:
        builder.build(sys.argv[1])
    elif len(sys.argv) == 1:
        builder.build('all')
    else:
        print >> sys.stderr,  "Usage: JSONMake [target]"
        sys.exit(1)
except subprocess.CalledProcessError as e:
    print >> sys.stderr, e.output
    sys.exit()
except KeyError:
    #Printing out a message was dealt with already
    sys.exit()

print "Build successful!"
