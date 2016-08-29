import time
import datetime
import threading
import pygame
import MrcLogger
from MrcPlayList import MrcPlayList
import MrcSettings

class MrcPlayer:

    def __init__(self):
        self.playlist=MrcPlayList()
        self.playing=False
        self.pausing=False
        self.wokenUp=False
        self.eventDequeuerThread=MrcPlayerEventDequeuer()
        self.lock=threading.RLock()

    def wakeUp(self):
        try:
            with self.lock:
                print ' ... MrcPlayerInstance waking up ...'
                MrcLogger.info(' ... MrcPlayerInstance waking up ...')
                pygame.init()
                pygame.mixer.init()
                self.eventDequeuerThread.start()
                pygame.mixer.music.set_endevent(pygame.USEREVENT)
                self.wokenUp=True
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.wakeUp: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.wakeUp: '+e.__str__())

    def goToSleep(self):
        try:
            with self.lock:
                print ' ... MrcPlayerInstance going to sleep ...'
                MrcLogger.info(' ... MrcPlayerInstance going to sleep ...')
                self.eventDequeuerThread.goToSleep()
                self.eventDequeuerThread.join()
                self.playlist.clean()
                pygame.mixer.quit()
                self.wokenUp=False
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.goToSleep: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.goToSleep: '+e.__str__())

    def playFile(self, mrcfile):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.playFile called while wokenUp is False! Not playing...')
                    return
                self.playlist.clean()
                self.playlist.addFile(mrcfile)
                self.playCurrent()
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.playFile('+filepath+'): '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.playFile('+filepath+'): '+e.__str__())

    def playFiles(self, mrcfiles):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.playFiles called while wokenUp is False! Not playing...')
                    return
                self.playlist.clean()
                self.playlist.addFileList(mrcfiles)
                self.playCurrent()
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.playFiles: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.playFiles: '+e.__str__())


    def stop(self):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.stop called while wokenUp is False! Not stopping...')
                    return
                if not ( self.playing or self.pausing ):
                    return
                pygame.mixer.music.stop()
                self.playing=False
                self.pausing=False
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.stop: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.stop: '+e.__str__())

    def playCurrent(self):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.playCurrent called while wokenUp is False! Not playing...')
                    return
                self.stop()
                curr=self.playlist.getCurrentFileName()
                if curr==None:
                    return
                pygame.mixer.music.load(curr)
                pygame.mixer.music.play() 
                self.playing=True
                self.pausing=False
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.playCurrent: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.playCurrent: '+e.__str__())

    def prev(self):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.prev called while wokenUp is False! Not going prev...')
                    return
                if not self.playlist.prev():
                    return
                self.playCurrent()
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.prev: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.prev: '+e.__str__())

    def next(self):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.next called while wokenUp is False! Not going next...')
                    return
                if not self.playlist.next():
                    return
                self.playCurrent()
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.next: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.next: '+e.__str__())

    def pause(self):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.pause called while wokenUp is False! Not pausing...')
                    return
                if self.playing and not self.pausing:
                    pygame.mixer.music.pause()
                    self.playing=False
                    self.pausing=True
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.pause: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.pause: '+e.__str__())

    def unpause(self):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.unpause called while wokenUp is False! Not unpausing...')
                    return
                if self.pausing and not self.playing:
                    pygame.mixer.music.unpause()
                    self.playing=True
                    self.pausing=False
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.unpause: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.unpause: '+e.__str__())

    def getPlayList(self):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.getPlayList called while wokenUp is False! Not getting playlist...')
                    return None, -1, False, 'Player not woken up, please try again later'
                files = []
                for f in self.playlist.files:
                    files.append(f)
                    if files[len(files)-1].path.startswith(MrcSettings.BASE_MUSIC_PATH):
                          files[len(files)-1].path=files[len(files)-1].path[len(MrcSettings.BASE_MUSIC_PATH):]
                return files, self.playlist.current, self.pausing, ''
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.getPlayList: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.getPlayList: '+e.__str__())

    def setVolumeUp(self):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.setVolumeUp called while wokenUp is False! Not setting volume up...')
                    return
                currentVolume = pygame.mixer.music.get_volume()
                if currentVolume < 0.95:
                    pygame.mixer.music.set_volume(currentVolume+0.05)
                elif currentVolume != 1.0:
                    pygame.mixer.music.set_volume(1.0)
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.setVolumeUp: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.setVolumeUp: '+e.__str__())

    def setVolumeDown(self):
        try:
            with self.lock:
                if not self.wokenUp:
                    MrcLogger.error('MrcPlayer.setVolumeDown called while wokenUp is False! Not setting volume down...')
                    return
                currentVolume = pygame.mixer.music.get_volume()
                if currentVolume > 0.05:
                    pygame.mixer.music.set_volume(currentVolume-0.05)
                elif currentVolume != 0.0:
                    pygame.mixer.music.set_volume(0.0)
        except pygame.error as e:
            MrcLogger.error('pygame.error caught in MrcPlayer.setVolumeDown: '+e.__str__())
        except Exception as e:
            MrcLogger.error('Exception caught in MrcPlayer.setVolumeDown: '+e.__str__())
 

    # TEST METHOD #
    def testStuff():
        try:
            file = 'C:\\partage\\mp3\\raph\\Muse\\Black Holes And Revelations\\Muse - 01 - Take A Bow.ogg'

            print str(datetime.datetime.now()) + ' ' + 'file: ' + file
            pygame.init()
            print str(datetime.datetime.now()) + ' ' + 'inited'
            pygame.mixer.init()
            print str(datetime.datetime.now()) + ' ' + 'mixer inited : ' + str(pygame.mixer.get_init())
            pygame.mixer.music.load(file)
            print str(datetime.datetime.now()) + ' ' + 'loaded'
            pygame.mixer.music.play()
            print str(datetime.datetime.now()) + ' ' + 'volume : ' + str(pygame.mixer.music.get_volume())
            print str(datetime.datetime.now()) + ' ' + 'playing'
            while pygame.mixer.music.get_busy(): 
                pygame.time.Clock().tick(10)
            print str(datetime.datetime.now()) + ' ' + 'finished'
            pygame.mixer.quit()
            print str(datetime.datetime.now()) + ' ' + 'quitted'

        except pygame.error as e:
            print 'pygame.error caught: '+e.__str__()
        except Exception as e:
            print 'Exception caught: '+e.__str__()


class MrcPlayerEventDequeuer(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stop=False
        self.lock=threading.Lock()

    def run(self):
        while not self.stop:
            time.sleep(1) #sleep 1s
            with self.lock:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT: 
                        self.stop=True
                        break
                    if event.type==pygame.USEREVENT:
                        instance().next()
                        continue

    def goToSleep(self):
        with self.lock:
            self.stop=True


MrcPlayerInstance=MrcPlayer()
def instance():
    return MrcPlayerInstance

