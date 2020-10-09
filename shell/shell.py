#! /usr/bin/env python3

import os
import sys
import re

def initialPrompt():
    while True:
        defaultPrompt = os.getcwd() + "$ "
        if 'PS1' in os.environ:
            defaultPrompt = os.environ['PS1']

        try:
            os.write(1, defaultPrompt.encode()) # writes the encoded default prompt with output file descriptor
            input = os.read(0,10000) # reads up to 10000 bytes
        except EOFError:
            sys.exit(1)


def executeCommand(input):
    if len(input) == 0: #contiues prompt if argument is empty
        continue
    if input[0].lower() == 'exit':
        sys.exit(0)
    if input[0].lower() == 'cd':
        try:
            os.chdir(args[1])
        except IndexError:
            os.write(2, ("You must include desired target directory \n").encode()) 
        except FileNotFoundError:
            os.write(2, ("No such directory found\n").encode()) #standard error file descriptor
    elif "|" in args:
        fork = os.fork()
        if fork == 0: #child process
            pipe(input)
        elif fork < 0:
            os.write(2, ("Fork failed\n").encode())
            sys.exit(1)
        else: #parent fork was good
            if input[-1] != "&":
                val = os.wait()
                if val[1] != 0 and val[1] != 256:
                    os.write(2, ("Program ended. Exit code: %d\n" % val[1].encode()))
            
    else:
        rc = os.fork()
        
        isWaiting = True

        if "&" in args:
            isWaiting = False
            args.remove("&")
        if rc == 0:
            redirectAndExecute(args)
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
        redirectAndExecute(read) #runs the process
        os.write(2, ("Not executable\n").encode())
        sys.exit(1)
    elif rc == 0: #child process
        os.close(1) #closes output file descriptor
        os.dup(pipeWriter,1) #dups pipe writer to file descriptor 1
        for fileDescriptor in (pipeReader, pipeWriter):
            os.close(fileDescriptor) #closes both pipe reader and pipe writer
        redirectAndExecute(write)  #runs the process
        os.write(2,("Not executable\n").encode())
        sys.exit(1)
    else: #fork failed
        os.write(2,("Fork failed\n").encode())
        sys.exit(1)

def redirectAndExecute(args):
    try:
        if '<' in args: #input redirection
            os.close(0) #input stdin
            os.open(args[args.index('<') +1], os.O_RDONLY) #opens file to read
            os.set_inheritable(0,True) #sets value of inheritable flag of stdin file descriptor
            args.remove(args[args.index('<')+1]) #removes file name from list
            args.remove('<') # removes > from list
            
        if'>' in args: #output redirection
            os.close(1) # output stdout
            os.open(args[args.index('>') +1], os.O_CREAT | os.O_WRONLY) #creates file to write
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

    for dir in re.split(":", os.environ['PATH']): #tries directories in path
        targetFile  = "%s%s" % (dir, args[0])
        try:
            os.execve(targetFile, args, os.environ)
        except FileNotFoundError:
            pass
        except Exception:
            sys.exit(1)
    os.write(2, ("Command not found\n").encode())
    sys.exit(1)
    
initialPrompt()
