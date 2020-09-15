#! /usr/bin/env python3

import os
import sys
import re

processID = os.getpid()

def initialPrompt():
    while(True):
        defaultPrompt = os.getcwd()
        if 'PS1'in os.environ:
            defaultPrompt = os.environ['PS1']
            
        command =input(defaultPrompt + ' $ ')
        comand = command.split(' ')
        if command[0].lower() == 'exit':
            sys.exit(0)
                
def runBuiltInCommands(userIn):
    if userIn[0] not in defaultCommands:
        return
    elif command == 'cd':
        currWorkingDir = os.getcwd() #gets current working directory
        if len(userIn)>1:
            try:
                os.chdir(os.path.join(cwd,command[1]))
            except FileNotFoundError:
                print("No such directory found")
            except NotADirectoryError:
                os.chdir(cwd) #keeps last cwd if user given directory is not found
initialPrompt()

        
