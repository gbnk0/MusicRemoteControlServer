import MrcPlayer
import MrcSettings

class CmdVolumeUpReply:
    def __init__(self):
        self.error=''

class CmdVolumeUp:
    def __init__(self):
        self.reply=CmdVolumeUpReply()

    def process(self):
        try:
            MrcPlayer.instance().setVolumeUp()
        except Exception as e:
            self.reply.error=e.__str__()

