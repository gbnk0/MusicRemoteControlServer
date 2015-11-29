import MrcPlayer
import MrcSettings

class CmdPlayListReply:
    def __init__(self):
        self.error=''
        self.files=[]
        self.currentFileIndex=-1
        self.isPaused=False

class CmdPlayList:
    def __init__(self):
        self.reply=CmdPlayListReply()

    def process(self):
        try:
            self.reply.files, self.reply.currentFileIndex, self.reply.isPaused, self.reply.error = MrcPlayer.instance().getPlayList()
        except Exception as e:
            self.reply.error=e.__str__()

