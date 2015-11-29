import os
import MrcPlayer
import MrcSettings

class CmdPlayDirQuery:
    def __init__(self):
        self.path=''

class CmdPlayDirReply:
    def __init__(self):
        self.error=''

class CmdPlayDir:
    def __init__(self, path):
        self.query=CmdPlayDirQuery()
        self.query.path=path
        self.files=[]
        self.reply=CmdPlayDirReply()

    def process(self):
        try:
            self.gatherMusicFiles(self.query.path)
            if not self.files:
                self.reply.error="no music file in: "+self.query.path
                return
            MrcPlayer.instance().playFiles(self.files)
        except Exception as e:
            self.reply.error=e.__str__()

    def gatherMusicFiles(self, dirPath):
        dirlisting = os.listdir(MrcSettings.BASE_MUSIC_PATH+dirPath)
        dirlisting.sort()
        for f in dirlisting:
            if os.path.isdir(MrcSettings.BASE_MUSIC_PATH+dirPath+MrcSettings.OS_SEPARATOR+f):
                self.gatherMusicFiles(dirPath+MrcSettings.OS_SEPARATOR+f)
            else:
                ismusicfile=False
                for ext in MrcSettings.MUSIC_FILE_EXTENSIONS:
                    if f.lower().endswith(ext):
                        ismusicfile=True
                        break
                if ismusicfile:
                    self.files.append(MrcSettings.BASE_MUSIC_PATH+dirPath+MrcSettings.OS_SEPARATOR+f)        
