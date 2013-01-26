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
            line_split = line.split()

            if line_split[1] == '=':
                #Everything following the '=' should be stored in a variable
                self.conversion_dict['Variables'][line_split[0]] = str.join(line_split[2:])

            if line_split[1] == ':':
                #This means that a rule is being declared
                rule = line_split[0]

                if len(line_split) > 2:
                    self.conversion_dict['Rules'][rule] = line_split[2:]
                else:
                    self.conversion_dict['Rules'][rule] = {}

            if line[0].isspace():
                #These are commands for some rule
                self.conversion_dict['Rules'][rule]['commands'].append(str.join(line_split))
