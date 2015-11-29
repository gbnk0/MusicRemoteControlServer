import MrcPlayer
import MrcSettings

class CmdPrevReply:
    def __init__(self):
        self.error=''

class CmdPrev:
    def __init__(self):
        self.reply=CmdPrevReply()

    def process(self):
        try:
            MrcPlayer.instance().prev()
        except Exception as e:
            self.reply.error=e.__str__()

