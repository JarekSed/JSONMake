import sys
import json
import functions

class MakeFileConverter:

    def __init__(self, makefile):
        self.makefile = makefile
        self.conversion_dict = {'Variables': {}, 'Rules': {}}

    def convert(self):
        #Performs the converting of makefile syntax to a Python dict

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
