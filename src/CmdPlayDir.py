import os
import MrcLogger
import MrcPlayer
import MrcSettings
import MrcFile
import CmdBrowse

class CmdPlayDirQuery:
    def __init__(self):
        self.fileid=''

class CmdPlayDirReply:
    def __init__(self):
        self.error=''

class CmdPlayDir:
    def __init__(self, fileid):
        self.query=CmdPlayDirQuery()
        self.query.fileid=fileid
        self.files=[]
        self.reply=CmdPlayDirReply()

    def process(self):
        try:
            currentFile=MrcFile.MrcFile('', True, False)

            if self.query.fileid:
                currentFile=MrcFile.getFromFileCache(self.query.fileid)
            if not currentFile.path:
                MrcLogger.error('failed to get file from cache with file id '+self.query.fileid)
                self.reply.error='failed to get file from cache with file id '+self.query.fileid
                return
            if not currentFile.isdir:
                self.reply.error='not a music directory: '+currentFile.path
                return

            self.gatherMusicFiles(currentFile)
            
            if not self.files:
                self.reply.error='no music file in: '+currentFile.path
                return

            MrcPlayer.instance().playFiles(self.files)
        except Exception as e:
            self.reply.error=e.__str__()

    def gatherMusicFiles(self, currentFile):
        if self.reply.error:
            return
        if currentFile.isdir:
            browseCmd=CmdBrowse.CmdBrowse(currentFile.fileid)
            browseCmd.process()
            if browseCmd.reply.error:
                self.reply.error = browseCmd.reply.error
                del self.files[:]
                return
            for f in browseCmd.reply.files:
                if f.isdir:
                    self.gatherMusicFiles(f)
                elif f.ismusicfile:
                    self.files.append(f) 

