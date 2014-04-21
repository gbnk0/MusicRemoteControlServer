import datetime
import pygame

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