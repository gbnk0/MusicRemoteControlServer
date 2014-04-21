import MrcLogger
import jsonpickle

from CmdBrowse import CmdBrowse

class MrcCommander:

    def __init__(self):
        self.cmd={}
        self.res=''

    def analyseReceivedLine(self, inputline):
        self.cmd={}
        try:
            if inputline.startswith('{'):
                self.cmd = jsonpickle.decode(inputline)
        except Exception as e:
            MrcLogger.info('Exception caught! '+e.__str__())

    def process(self):
        if 'command' not in self.cmd:
            MrcLogger.error('MrcCommander failed to parse incoming query: no "command" key!')
            return
        if self.cmd['command']=='Browse':
            if 'path' not in self.cmd:
                MrcLogger.error('MrcCommander failed to parse CmdBrowse incoming query: no "path" key!')
                return
            c=CmdBrowse(self.cmd['path'])
            c.process()
            self.res=jsonpickle.encode(c.reply, unpicklable=False)
