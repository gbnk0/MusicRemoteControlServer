import MrcSettings
import MrcLogger

class MrcFile:

    def __init__(self, filepath, isdir, ismusicfile):
        self.path=filepath
        self.fileid=''
        self.isdir=isdir
        self.ismusicfile=ismusicfile
        self.sortingname=''
        self.displayname=''

    def getFileNameFromPath(self):
        pathsplit = self.path.split(MrcSettings.OS_SEPARATOR)
        return pathsplit[len(pathsplit)-1]

    def getSortingName(self):
        if self.sortingname:
            return self.sortingname
        name = self.getFileNameFromPath()
        self.sortingname = name.lower()
        return self.sortingname

    def getDisplayName(self):
        if self.displayname:
            return self.displayname
        name = self.getFileNameFromPath()
        self.displayname = name
        return self.displayname

    def setFileId(self, parentfileid, currentincrement):
        self.fileid = ''
        if parentfileid:
            self.fileid = parentfileid + '-'
        self.fileid += str(currentincrement).zfill(3)

############################

MrcFileCache = {}

def addToFileCache(mf):
    if mf.fileid:
        MrcFileCache[mf.fileid]=mf
    else:
        MrcLogger.error('Tried to add file to cache with empty id: '+mf.filepath) 

def getFromFileCache(fileid):
    return MrcFileCache[fileid]


