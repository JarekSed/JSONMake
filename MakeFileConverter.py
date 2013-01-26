import sys
import json
import functions

class MakeFileConverter:
    """
    A class that deals with converting regular Makefiles to JSONMakefiles

    Methods:
    convert(): Converts the Makefile
    """

    def __init__(self, makefile=functions.openIgnoreCase("Makefile")):
        self.makefile = makefile
        self.conversion_dict = {'Variables': {}, 'Rules': {}}

    def convert(self):
        """
        Converts the Makefile into a JSONMakeFile
        """

        rule = ''

        for line in self.makefile:

            if line == '' or line.isspace():
                continue

            if '=' in line:
                #Everything following the '=' should be stored in a variable
                var_split = line.split('=')
                self.conversion_dict['Variables'][var_split[0].strip()] = var_split[1].strip()

            if ':' in line:
                #This means that a rule is being declared
                rule_split = line.split(':')
                rule = rule_split[0].strip()
                try:
                    self.conversion_dict['Rules'][rule]['depends'].append(rule_split[1].strip())
                except KeyError:
                    self.conversion_dict['Rules'][rule] = {'depends': [], 'commands': []}
                    self.conversion_dict['Rules'][rule]['depends'].append(rule_split[1].strip())

            if line[0].isspace():
                #These are commands for some rule
                #Everything after the initial whitespace is a command
                self.conversion_dict['Rules'][rule]['commands'].append(' '.join(line.split()))

        __writeFile()

    def __writeFile(self):
        with open('JSONMakefile', 'w') as file:
            #write the actual file...I'm going to bed for now though
