import MrcPlayer
import MrcSettings

class CmdPlayFileQuery:
    def __init__(self):
        self.path=''

class CmdPlayFileReply:
    def __init__(self):
        self.error=''

class CmdPlayFile:
    def __init__(self, path):
        self.query=CmdPlayFileQuery()
        self.query.path=path
        self.reply=CmdPlayFileReply()

    def process(self):
        try:
            ismusicfile=False
            for ext in MrcSettings.MUSIC_FILE_EXTENSIONS:
                if self.query.path.lower().endswith(ext):
                    ismusicfile=True
                    break
            if ismusicfile:
                MrcPlayer.instance().playFile(MrcSettings.BASE_MUSIC_PATH+self.query.path)
            else:
                self.reply.error="not a music file: "+self.query.path
        except Exception as e:
            self.reply.error=e.__str__()
