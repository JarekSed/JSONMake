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

        if '$' in line:
            #Strip parentheses for all words in the line that has a dollar sign
            newLine = ""
            for word in line.split():
                if '$' in word:
                    newLine += __parenStrip(word) + " "
                else:
                    newLine += word + " "
            if line[0].isspace():
                line = line[0] + newLine
            else:
                line = newLine

        if '=' in line:
            #Everything following the '=' should be stored in a variable
            var_split = line.split('=')
            if len(var_split) > 2:
                variable = "=".join(var_split[1:]).strip()
            else:
                variable = var_split[1].strip()
            conversion_dict['Variables'][var_split[0].strip()] = __parenStrip(variable)

        if ':' in line:
            #This means that a rule is being declared
            rule_split = line.split(':')
            rule = rule_split[0].strip()

            try:
                conversion_dict['Rules'][rule]['depends'].extend([word for word in rule_split[1].split()])
            except KeyError:
                conversion_dict['Rules'][rule] = {'depends': [], 'commands': []}
                conversion_dict['Rules'][rule]['depends'].extend([word for word in rule_split[1].split()])

        if line[0].isspace():
            #These are commands for some rule
            #Everything after the initial whitespace is a command
            conversion_dict['Rules'][rule]['commands'].append(' '.join(line.split()))

    __writeFile(conversion_dict)

def __writeFile(conversion_dict):
    """
    Writes the makefile to file

    Accepts a dictionary as input, and converts to a json object, then writes to the file
    """

    with open('JSONMakefile', 'w') as file:
        #write the actual file
        file.write(json.dumps(conversion_dict, sort_keys=True, indent=4, separators=(',', ': ')))

def __parenStrip(string):
    """
    Strips the parentheses enclosing a variable
    I'll deal with other cases later, but for now it is up to the user to match parentheses correctly
    """
    print string
    if not ('(' in string and ')' in string):
        return string

    if string[1] == '(' and string[-1] == ')':
        return string[0] + string[2:-1]
    return string
