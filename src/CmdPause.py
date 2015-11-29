import MrcPlayer
import MrcSettings

class CmdPauseReply:
    def __init__(self):
        self.error=''

class CmdPause:
    def __init__(self):
        self.reply=CmdPauseReply()

    def process(self):
        try:
            MrcPlayer.instance().pause()
        except Exception as e:
            self.reply.error=e.__str__()

