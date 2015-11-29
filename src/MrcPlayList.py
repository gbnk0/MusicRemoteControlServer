import threading

class MrcPlayList:

    def __init__(self):
        self.files=[]
        self.current=-1
        self.lock=threading.RLock()

    def addFile(self, newFile):
        with self.lock:
            wasEmpty=not self.files
            self.files.append(newFile)
            if wasEmpty:
                self.current=0

    def removeFile(self, index):
        with self.lock:
            if self.files and index>=0 and index<len(self.files):
                del self.files[index]
                if not self.files:
                    self.current=-1
                elif index<=self.current:
                    self.current-=1

    def addFileList(self, newFiles):
        with self.lock:
            wasEmpty=not self.files
            self.files.extend(newFiles)
            if wasEmpty:
                self.current=0

    def clean(self):
        with self.lock:
            del self.files[:]
            self.current=-1

    def next(self):
        with self.lock:
            if self.files and self.current>=0 and self.current<len(self.files)-1:
                self.current+=1
                return True 
            else:
                return False

    def prev(self):
        with self.lock:
            if self.files and self.current>0 and self.current<len(self.files):
                self.current-=1
                return True 
            else:
                return False

    def getCurrentFileName(self):
        with self.lock:
            if self.files and self.current>=0 and self.current<len(self.files):
                return self.files[self.current]
            else:
                return None
