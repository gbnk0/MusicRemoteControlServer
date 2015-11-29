import MrcPlayer
import MrcSettings

class CmdNextReply:
    def __init__(self):
        self.error=''

class CmdNext:
    def __init__(self):
        self.reply=CmdNextReply()

    def process(self):
        try:
            MrcPlayer.instance().next()
        except Exception as e:
            self.reply.error=e.__str__()

