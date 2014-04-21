import sys
import os
import datetime
import threading

MrcLogFilePath='../log/log.txt'
MrcLogLock=threading.Lock()
MrcLog=open(MrcLogFilePath,'a')

def startToLog():
    MrcLogLock.acquire()

def stopToLog():
    MrcLog.flush()
    os.fsync(MrcLog.fileno())
    MrcLogLock.release()

def info(line):
    startToLog()
    MrcLog.write(str(datetime.datetime.now()) + ' ' + line + '\n')
    stopToLog()

def error(line):
    startToLog()
    MrcLog.write(str(datetime.datetime.now()) + ' [ERROR] ' + line + '\n')
    stopToLog()