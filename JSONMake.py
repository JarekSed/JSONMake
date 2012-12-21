'''
Python script to parse JSON makefiles. I'll add good doc strings later

@author: Sam Agnew
'''
import sys
import json
import subprocess
import os
	
#Eventually I plan to allow the user to input a file name(perhaps even a path to the JSONMakefile in another directory?
def openIgnoreCase(file_name):
	"""
	Opens a file, ignoring case for the file name.
	
	Arguments:
	file_name: The name of the file to be opened.
	"""

	files = os.listdir(os.curdir)
	#iterate through every file in the directory
	for file in files:
		if file.lower() == file_name.lower():
			return open(file)
	#If the loop is exited, then this file is not in the directory.
	print "Error! no JSONMakefile in this directory!"
	sys.exit()

def isFileInDir(file_name):
	"""
	Checks to see whether a file is in the current directory
	
	Arguments:
	file_name: The name of the file.
	"""

	files = os.listdir(os.curdir)
	return file_name in files

class JSONMaker:
	
	"""
	A class that deals with makefile functionality.
	
	Methods:
	replaceVar(string)
	build(rule)
	"""

	def __init__(self, json_object):
		self.__json_object = json_object
		return

	def replaceVar(self, string):

		"""
		Takes an input string that represents a variable, and replaces it with it's corresponding value
		
		The variable will usually have a preceding $ char to denote that it is a variable, but this should be dealt with before calling this method.
		Arguments:
		string: The variable to be replaced
		"""
		
		try:
			return self.__json_object['Variables'][string]
		except KeyError:
			print "Invalid JSON Object! Check your variables"
			sys.exit()

	def build(self, rule):
		
		"""
		Attempts to recursively build from a rule

		Arguments:
		rule: String representing the name of the rule
		"""

		try:
			#This makes the rest of my code easier to read
			thisRule = self.__json_object['Rules'][rule]
		except KeyError:
			print "Rule not found: " + rule
			sys.exit()

		if 'depends' in thisRule:
			if thisRule['depends'] not in self.__json_object['Rules']:
				if isFileInDir(thisRule['depends']):
					return True
				else:
					print "File not found: " + thisRule['depends']
					sys.exit()
			else:
				try:
					self.build(thisRule['depends'])
				except subprocess.CalledProcessError as e:
					raise e

		if 'commands' in thisRule:
			commands = thisRule['commands']

			#Go through every command and run each one separately
			for command in commands:
				
				#Replace all variables in the commands string
				for word in command.split():
					if word[0] == '$':
						#send in the word without the preceding '$'
						word = self.replaceVar(word[1:])
				
				#Actually execute the commands	
				try:
					self.execute_command(command.split())
				except subprocess.CalledProcessError as e:
					raise e

	#Executes the command given. The command argument should be in list form.
	def execute_command(self, command):
		try:
			return subprocess.check_call(command)
		except subprocess.CalledProcessError as e:
			raise e.returncode

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
