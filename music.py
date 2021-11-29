import playsound
from pynput import keyboard

# JINGLE BELLS
# E E E - E E E - E G C D E - - -
# F  F  F  F  F E E EE
# E D D E D - G
# E E E - E E E - E G C D E - - -
# F  F  F  F  F E E EE
# G G F D C

def on_press(key):
    try:
        # print('alphanumeric key {0} pressed'.format(key.char))
        try:    
            playsound.playsound('./notes/{0}3.mp3'.format(key.char), False)
        except playsound.PlaysoundException as err:
            pass
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def entry():
    # Collect events until released
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()

def main():
    entry()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Quit")