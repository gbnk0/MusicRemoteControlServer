import MrcPlayer
import MrcSettings

class CmdVolumeDownReply:
    def __init__(self):
        self.error=''

class CmdVolumeDown:
    def __init__(self):
        self.reply=CmdVolumeDownReply()

    def process(self):
        try:
            MrcPlayer.instance().setVolumeDown()
        except Exception as e:
            self.reply.error=e.__str__()

