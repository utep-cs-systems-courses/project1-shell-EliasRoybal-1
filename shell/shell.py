import os
import sys
import re

def initialPrompt():
    global processID
    processID = os.getpid()
    while 1:
        userIn =input("$ ")
        if userIn == "exit":
            break
        try:
            command = eval(userIn)
            print(processID)
            if command: print(command)
        except:
            try:
                exec(userIn)
            except Exception as e:
                print("Error: ", e)
                
initialPrompt()

