import os

import MrcLogger
import MrcSettings

class CmdBrowseQuery:
    def __init__(self):
        self.path=''

class CmdBrowseReply:
    def __init__(self):
        self.files=[]
        self.error=''

class CmdBrowse:
    def __init__(self, path):
        self.query=CmdBrowseQuery()
        self.query.path=path
        self.reply=CmdBrowseReply()

    def process(self):
        try:
            # MrcLogger.debug('CmdBrowse process('+self.query.path+')')
            for f in os.listdir(MrcSettings.BASE_MUSIC_PATH+self.query.path):
                if os.path.isdir(MrcSettings.BASE_MUSIC_PATH+self.query.path+MrcSettings.OS_SEPARATOR+f):
                    self.reply.files.append(f)
                else:
                    ismusicfile=False
                    for ext in MrcSettings.MUSIC_FILE_EXTENSIONS:
                        if f.lower().endswith(ext):
                            ismusicfile=True
                            break
                    if ismusicfile:
                        self.reply.files.append(f)
            self.reply.files.sort()
        except Exception as e:
            self.reply.error=e.__str__()
