#! /usr/bin/env python3

import os
import sys
import re

processID = os.getpid()

def initialPrompt():
    while True:
        cwd = os.getcwd()
        if 'PS1'in os.environ:
            defaultPrompt = os.environ['PS1']
            
        args =input(cwd + ' $ ')
        args = args.strip()
        args = args.split(' ')

        try:

            if len(args) == 0: #contiues prompt in argument is empty
                continue
            if args[0].lower() == 'exit':
                sys.exit(0)
                if args[0].lower() == 'cd':
                    try:
                        os.chdir(args[1])
                    except IndexError:
                        os.write(2, ("You must include desired target directory \n").encode()) 
                    except FileNotFoundError:
                        os.write(2, ("No such directory found\n").encode()) #standard error file descriptor
                elif "|" in args:
                    fork = os.fork()
                    if fork == 0: #child process
                        pipe(args)
                    elif fork < 0:
                        os.write(2, ("Fork failed\n").encode())
                        sys.exit(1)
                    else: #parent for was good
                        if args[-1] != "&":
                            val = os.wait()
                            if val[1] != 0 and val[1] != 256:
                                os.write(2, ("Program ended. Exit code: %d\n" % val[1].encode()))
        except FileNotFoundError:
            sys.exit(1)
        else:
            rc = os.fork()

            isWaiting = True

            if "&" in args:
                isWaiting = False
                args.remove("&")
            if rc == 0:
                redirectionAndExecution(args)
            elif rc < 0:
                os.write(2,("Fork failed".encode()))
                sys.exit(1)

            else:
                if isWaiting:
                    val = os.wait()
                    if val[1] !=0 and val[1] != 256:
                        os.write(2,("Program terminated. Exit Code: %d\n" % val[1]).encode())
                        
def pipe(args):
    write = args[0:args.index("|")]
    read = args[args.index("|")+1:]
    pipeReader, pipeWriter = os.pipe()
    rc = os.fork(); #returns 0 to child, pid to parent

    if rc > 0: #parent process
        os.close(0)#closes input file descriptor
        os.dup(pipeReader,0) #dups pipe reader to file descriptor 0
        for fileDescriptor in (pipeWriter, pipeReader):
            os.close(fileDescriptor) #closes with file descriptor in pipe
        if "|" in read:
            pipe(read)
        initialPrompt() #runs going back to initialPrompt
        os.write(2, ("Not executable\n").encode())
        sys.exit(1)
    elif rc == 0: #child process
        os.close(1) #closes output file descriptor
        os.dup(pipeWriter,1) #dups pipe writer to file descriptor 1
        for fileDescriptor in (pipeReader, pipeWriter):
            os.close(fileDescriptor) #closes both pipe reader and pipe writer
        initialPrompt() #goes back to initialPrompt
        os.write(2,("Not executable\n").encode())
        sys.exit(1)
    else: #fork failed
        os.write(2,("Fork failed\n").encode())
        sys.exit(1)

def redirectionAndExecution(args):
    try:
        if '<' in args: #input redirection
            os.close(0) #input stdin
            os.open(args[args.index('<') +1], os.O_RDONLY) #opens file to read
            os.set_inheritable(0,true) #sets value of inheritable flag of stdin file descriptor
            args.remove(args[args.index('<')+1]) #removes file name from list
            args.remove('<') # removes > from list
            
        if'>' in args: #output redirection
            os.close(1) # output stdout
            os.open(args[args.index('>') +1], os,O_CREAT | os.O_WRONLY) #creates file to write
            os.set_inheritable(1,True)#sets vaue of inheritbale flag of stdout file descriptor
            args.remove(args[args.index('>')+1]) #removes file name
            args.remove('>') # removes >
    except IndexError:
        os.write(2, "Not able to redirect\n")
    try:
        if args[0][0] == '/':
            os.execve(args[0],args,os.environ) #tries to run process
    except FileNotFoundError:
        pass
    except Exception:
        sys.exit(1)

    os.write(2,("Command not found\n").encode())
    sys.exit(1)
    
initialPrompt()
