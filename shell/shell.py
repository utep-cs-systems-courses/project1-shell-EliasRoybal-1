import os
import sys
import re

processID = os.getpid()
defaultCommands =['cd','exit']
def initialPrompt():
    defaultPrompt = '$ '
    if 'PS1'in os.environ:
        print("in if")
        defaultPrompt = os.environ['PS1'] #makes the default prompt contain the default environment variable
        
    while True:
        userIn =input(defaultPrompt)
        if userIn == "exit":
            sys.exit(0)
        try:
            command = eval(userIn)
            fork =  os.fork()
            if fork > 0:
                print("Parent process ID:" ,processID)
            else:
                print("Child process ID:", processID)
            #print(processID)
            if command: print(command)
        except KeyError as e:
            print("Error: ", e)
        except:
            try:
                exec(userIn)
            except Exception as e:
                print("Error: ", e)
                
initialPrompt()
        
