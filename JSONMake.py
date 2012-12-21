'''
Python script to parse JSON makefiles. I'll add good doc strings later

@author: Sam Agnew
'''
import sys
import json
import subprocess
import os
from functions import *
from JSONMaker import *

try:
    with openIgnoreCase('JSONMakefile') as f:
        makeFile = json.load(f)
except EnvironmentError:
    print "JSON MakeFile not found!"
    sys.exit()
except ValueError:
	print "Invalid JSON object!"
	sys.exit()

builder = JSONMaker(makeFile)

#Decided to make this and 'all' two separate cases. Does this affect readability, and make things too cluttered?
if 'Rules' not in makeFile:
	sys.exit()

#Just to check if there is a rule to build for 'all' 
if 'all' in makeFile['Rules']:
	try:
		builder.build('all')
	except subprocess.CalledProcessError as e:
		print "fuck"
		print e.output
		sys.exit()
else:
	print "No rule to build 'all'!"
	sys.exit()
