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
        command = command.strip()
        comand = command.split(' ')
        
        if command.lower() == 'exit':
            sys.exit(0)
        if command == 'cd':
            currWorkingDir = os.getcwd() #gets current working directory
            if len(command)>1:
                try:
                    os.chdir(os.path.join(defaultPrompt,command[1]))
                except FileNotFoundError:
                    print("No such directory found")
                except NotADirectoryError:
                    os.chdir(cwd) #keeps last cwd if user given directory is not found
initialPrompt()

        
