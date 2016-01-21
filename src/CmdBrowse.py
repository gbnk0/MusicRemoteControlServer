import os

import MrcLogger
import MrcSettings
import MrcFile

class CmdBrowseQuery:
    def __init__(self):
        self.fileid=''

class CmdBrowseReply:
    def __init__(self):
        self.currentFolder=MrcFile.MrcFile('', True, False)
        self.files=[]
        self.error=''

class CmdBrowse:

    def __init__(self, fileid):
        self.query=CmdBrowseQuery()
        self.query.fileid=fileid
        self.reply=CmdBrowseReply()

    def process(self):
        self.processByFileId()

    def processByFileId(self):
        try:
            pathToBrowse=MrcSettings.BASE_MUSIC_PATH
            if self.query.fileid:
                self.reply.currentFolder=MrcFile.getFromFileCache(self.query.fileid) 
                pathToBrowse+=self.reply.currentFolder.path
            if not pathToBrowse:
                MrcLogger.error('failed to get file from cache with file id '+self.query.fileid)
                self.error='failed to get file from cache with file id '+self.query.fileid
            i=0
            for f in os.listdir(pathToBrowse):
                i+=1
                fpath=pathToBrowse+MrcSettings.OS_SEPARATOR+f
                fpath=fpath[len(MrcSettings.BASE_MUSIC_PATH):]
                if fpath.startswith(MrcSettings.OS_SEPARATOR):
                    fpath=fpath[len(MrcSettings.OS_SEPARATOR):]
                if os.path.isdir(pathToBrowse+MrcSettings.OS_SEPARATOR+f):
                    mf=MrcFile.MrcFile(fpath, True, False)
                    mf.setFileId(self.query.fileid, i)
                    mf.getDisplayName()
                    self.reply.files.append(mf)
                    MrcFile.addToFileCache(mf)
                else:
                    ismusicfile=False
                    for ext in MrcSettings.MUSIC_FILE_EXTENSIONS:
                        if f.lower().endswith(ext):
                            ismusicfile=True
                            break
                    if ismusicfile:
                        mf=MrcFile.MrcFile(fpath, False, True)
                        mf.setFileId(self.query.fileid, i)
                        mf.getDisplayName()
                        self.reply.files.append(mf)
                        MrcFile.addToFileCache(mf)
            self.reply.files=sorted(self.reply.files, key=lambda mf:mf.getSortingName())
        except Exception as e:
            self.reply.error=e.__str__()

