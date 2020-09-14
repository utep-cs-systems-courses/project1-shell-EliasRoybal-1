import os
import sys
import re

processID = os.getpid()
def initialPrompt():
    while 1:
        userIn =input("$ ")
        if userIn == "exit":
            break
        try:
            fork =  os.fork()
            if fork > 0:
                print("Parent process ID:" ,processID)
            else:
                print("Child process ID:", processID)
            command = eval(userIn)
            #print(processID)
            if command: print(command)
        except:
            try:
                exec(userIn)
            except Exception as e:
                print("Error: ", e)
                
initialPrompt()
