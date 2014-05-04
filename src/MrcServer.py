import os
import sys
import time

import MrcLogger
import MrcHttpServer
import MrcPlayer

###################

def usage():
    print 'Example:'
    print ' > python MrcServer.py 8080'

def interpret(userinput):
    userinput=userinput.strip()
    MrcLogger.info('userinput ['+userinput+']')
    if(userinput=='Q'):
        return False
    return True

###################
###### MAIN #######
###################

print
print '---------- MusicRemoteControlServer ------------'
print 
MrcLogger.info('---------- MusicRemoteControlServer ------------')

if len(sys.argv)!=2:
    print 'ERROR: you need to specify a port number as first argument!!'
    MrcLogger.error('no first argument for specifying the port number : exiting...')
    usage()
    exit()

portnum=0
try:
    portnum=int(sys.argv[1])
except ValueError:
    print 'ERROR: you need to specify a port number as first argument!!'
    MrcLogger.error('first argument failed to be parsed as a port number : exiting...')
    usage()
    exit()

httpserverthread = MrcHttpServer.MrcHTTPServerThread(portnum)
httpserverthread.start()

MrcPlayer.instance().wakeUp()

time.sleep(2)

userinput=''
while(not userinput):
    sys.stdout.write(' > ')
    userinput=sys.stdin.readline()
    if(not interpret(userinput)):
        break
    userinput=''

MrcPlayer.instance().goToSleep()
httpserverthread.server.shutdown()

time.sleep(2)
print 'Thanks for using MusicRemoteControlServer! See you soon!'
exit()