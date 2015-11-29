import MrcPlayer
import MrcSettings

class CmdUnpauseReply:
    def __init__(self):
        self.error=''

class CmdUnpause:
    def __init__(self):
        self.reply=CmdUnpauseReply()

    def process(self):
        try:
            MrcPlayer.instance().unpause()
        except Exception as e:
            self.reply.error=e.__str__()

