'''
Python script to parse JSON makefiles. I'll add good doc strings later

@author: Sam Agnew
'''
import sys
import json
import subprocess

#A class containing various methods to help me deal with files effectively
class FileUtilities:
    
    def __init__(self):
        return
    
	#Opens a file, ignoring case for the file name 
    def openIgnoreCase(self, file_name):
        return open(file_name)

#A class that deals with makefile functionality
class Builder:
	
	def __init__(self, json_object):
		self.__json_object = json_object
		return

	#Takes an input string(with a preceding $ char to denote that it is a variable) and replaces it with it's corresponding value
	def replaceVar(self, string):
		return self.__json_object['Variables'][string[1:]]

	#Attempts to build from a rule with the input string as a name of the rule
	def build(self, rule):

		#This makes the rest of my code easier to read
		thisRule = self.__json_object['Rules'][rule]

		if 'depends' in thisRule:
			self.build(thisRule['depends'])
		
		#This is the string with the commands in this JSON object
		commands = thisRule['commands']

		for command in commands:
			
			#Replace all variables in the commands string
			for word in command.split():
				if word[0] == '$':
					word = replaceVar(word)
			
			#Actually execute the commands		
			try:
				subprocess.check_call(command.split())
			except subprocess.CalledProcessError as e:
				print e.output
				return e.returncode
			return 


utilities = FileUtilities() #object to deal with files

try:
    with utilities.openIgnoreCase('JSONMakefile') as f:
        makeFile = json.load(f)
except EnvironmentError:
    print "JSON MakeFile not found!"
    sys.exit()
except ValueError:
	print "Invalid JSON object!"
	sys.exit()

builder = Builder(makeFile)

#Just to check if there is a rule to build for 'all'
try:
	makeFile['Rules']['all']
except KeyError:
	print "No rule for 'all'!"
	sys.exit()

builder.build('all')

