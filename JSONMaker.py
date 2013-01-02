import json
import subprocess
import functions

class JSONMaker:
    
    """
    A class that deals with makefile functionality.
    
    Methods:
    replaceVar(string)
    build(rule)
    """

    def __init__(self, json_object):
        self.__json_object = json_object
        if 'Rules' not in json_object:
            print >> sys.stderr, "Invalid make file! Please include 'Rules'"
            raise IOError

    def __replaceVar(self, string):

        """
        Takes an input string that represents a variable, and replaces it with it's corresponding value
        
        The variable will usually have a preceding $ char to denote that it is a variable, but this should be dealt with before calling this method.
        Arguments:
        string: The variable to be replaced
        """
        
        try:
            return self.__json_object['Variables'][string]
        except KeyError:
            print >> sys.stderr, "Invalid JSON Object! Check your variables"
            raise KeyError

    def build(self, rule):
        
        """
        Attempts to recursively build from a rule

        Arguments:
        rule: String representing the name of the rule
        """
    
        thisRule = ""

        if functions.isFileInDir(rule):
            thisRule = rule
            #This already exists, and nothing needs to be done for now. 
            return True
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
                        for replacement in self.__replaceVar(word[1:]).split():
                            command_to_execute.append(replacement)
                    else:
                        command_to_execute.append(word)

                #Actually execute the commands  
                try:
                    print "Execute: " + str(command_to_execute)
                    self.__execute_command(command_to_execute)
                except subprocess.CalledProcessError as e:
                    raise e

    def __execute_command(self, command):
        """
        Executes the command given. The command argument should be in list form.

        Arguments:
        command: The command to be executed.
        """
        try:
            return subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            raise e
