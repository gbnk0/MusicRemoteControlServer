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
            for f in os.listdir(MrcSettings.BASE_MUSIC_PATH+self.query.path):
                if os.path.isdir(MrcSettings.BASE_MUSIC_PATH+self.query.path+f) or f.endswith('.mp3') or f.endswith('.ogg'):
                    self.reply.files.append(f)
        except Exception as e:
            self.reply.error=e.__str__()
