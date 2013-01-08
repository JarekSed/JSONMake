import os
import sys

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
    raise IOError

def isFileInDir(file_name):
    """
    Checks to see whether a file is in the current directory

    Arguments:
    file_name: The name of the file.
    """

    files = os.listdir(os.curdir)
    return file_name in files

