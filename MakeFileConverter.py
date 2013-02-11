import sys
import json
import functions

def convert(makefile_name="Makefile"):
    """
    Converts the Makefile into a JSONMakeFile
    """

    makefile=functions.openIgnoreCase(makefile_name)
    conversion_dict = {'Variables': {}, 'Rules': {}}

    rule = ''

    for line in makefile:

        if line == '' or line.isspace():
            continue

        if '=' in line:
            #Everything following the '=' should be stored in a variable
            var_split = line.split('=')
            conversion_dict['Variables'][var_split[0].strip()] = "=".join(var_split[1:]).strip()

        if ':' in line:
            #This means that a rule is being declared
            rule_split = line.split(':')
            rule = rule_split[0].strip()
            try:
                conversion_dict['Rules'][rule]['depends'].append(rule_split[1].strip())
            except KeyError:
                conversion_dict['Rules'][rule] = {'depends': [], 'commands': []}
                conversion_dict['Rules'][rule]['depends'].append(rule_split[1].strip())

        if line[0].isspace():
            #These are commands for some rule
            #Everything after the initial whitespace is a command
            conversion_dict['Rules'][rule]['commands'].append(' '.join(line.split()))

    __writeFile()

def __writeFile(self):
    with open('JSONMakefile', 'w') as file:
        #write the actual file...I'm going to bed for now though
        return
