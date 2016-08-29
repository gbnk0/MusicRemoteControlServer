import MrcPlayer
import MrcSettings
import MrcFile

class CmdPlayFileQuery:
    def __init__(self):
        self.fileid=''

class CmdPlayFileReply:
    def __init__(self):
        self.error=''

class CmdPlayFile:
    def __init__(self, fileid):
        self.query=CmdPlayFileQuery()
        self.query.fileid=fileid
        self.reply=CmdPlayFileReply()

    def process(self):
        try:
            currentFile=MrcFile.MrcFile('', True, False)
            if self.query.fileid:
                currentFile=MrcFile.getFromFileCache(self.query.fileid)
            if not currentFile.path:
                MrcLogger.error('failed to get file from cache with file id '+self.query.fileid)
                self.error='failed to get file from cache with file id '+self.query.fileid
            if currentFile.ismusicfile:
                MrcPlayer.instance().playFile(currentFile)
            else:
                self.reply.error='not a music file: '+currentFile.path
        except Exception as e:
            self.reply.error=e.__str__()
