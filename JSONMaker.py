import json
import subprocess
import functions
import os
import sys

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

    def __needsToBeBuilt(self, rule):

        """
        Checks to see if a rule needs to be built.
        This is based on when the rule was last modified compared to it's dependencies.
        It is assumed that the rule exists, because that check should have been already made.

        Arguments:
        rule - String representing the name of the rule
        """

        thisRule = self.__json_object['Rules'][rule]
        time_last_modified = os.path.getmtime(rule)

        if 'depends' in thisRule:
            for dependency in thisRule['depends'].split():

                #In all of the following cases, it is decided that the rule must be built.
                #If none of them are true for all dependencies of a rule, then False is returned.
                if not functions.isFileInDir(dependency):
                    #This means that the dependency does not exist in the directory.
                    return True

                if time_last_modified < os.path.getmtime(dependency):
                    #This means that a dependency has been modified.
                    return True

                if dependency in self.__json_object['Rules'] and self.__needsToBeBuilt(dependency):
                    #Now a recursive check is made for every dependency of this rule
                    return True

        #None of the other cases returned True
        return False

    def build(self, rule):

        """
        Attempts to recursively build from a rule

        Arguments:
        rule: String representing the name of the rule
        """

        thisRule = ""

        if functions.isFileInDir(rule):
            if rule not in self.__json_object['Rules']:
                #There is no rule for this. Nothing needs to be done.
                return
            else:
                if not self.__needsToBeBuilt(rule):
                    return

        try:
            thisRule = self.__json_object['Rules'][rule]
        except KeyError:
            print >> sys.stderr, "Rule not found: " + rule
            raise KeyError

        if 'depends' in thisRule:
            for dependency in thisRule['depends'].split():
                try:
                    self.build(dependency)
                except subprocess.CalledProcessError as e:
                    raise e

        if 'commands' in thisRule:
            commands = thisRule['commands']

            #Go through every command and run each one separately
            for command in commands:
                command_to_execute = []

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
                    print "Executing: " + " ".join(command_to_execute)
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
