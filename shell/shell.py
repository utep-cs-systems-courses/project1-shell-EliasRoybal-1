import os
import sys
import re

while 1:
    userIn =input("$ ")
    if userIn == "exit":
        break
    try:
        command = eval(userIn)
        if command: print(command)
    except:
        try:
            exec(userIn)
        except Exception as e:
            print("Error: ", e)
