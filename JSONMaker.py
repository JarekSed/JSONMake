import json
import subprocess
from functions import *

class JSONMaker:
	
	"""
	A class that deals with makefile functionality.
	
	Methods:
	replaceVar(string)
	build(rule)
	"""

	def __init__(self, json_object):
		self.__json_object = json_object

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
			raise KeyError

	def build(self, rule):
		
		"""
		Attempts to recursively build from a rule

		Arguments:
		rule: String representing the name of the rule
		"""
	
		thisRule = ""

		if isFileInDir(rule):
			thisRule = rule
		else:
			try:
				thisRule = self.__json_object['Rules'][rule]
			except KeyError:
				print "Rule not found: " + rule
				raise KeyError

		if 'depends' in thisRule:
			for dependency in thisRule['depends'].split():
				try:
					self.build(dependency)
				except subprocess.CalledProcessError as e:
					raise e

		if 'commands' in thisRule:
			commands = thisRule['commands']
			command_to_execute = []

			#Go through every command and run each one separately
			for command in commands:
				
				#Replace all variables in the commands string
				for word in command.split():
					if word[0] == '$':
						#send in the word without the preceding '$'
						command_to_execute.append(self.replaceVar(word[1:]))
					else:
						command_to_execute.append(word)

				#Actually execute the commands	
				try:
					self.execute_command(command_to_execute)
				except subprocess.CalledProcessError as e:
					raise e

		return None
	
	def execute_command(self, command):
		"""
		Executes the command given. The command argument should be in list form.

		Arguments:
		command: The command to be executed.
		"""
		try:
			return subprocess.check_call(command)
		except subprocess.CalledProcessError as e:
			raise e
