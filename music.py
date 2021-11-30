from pynput import keyboard
import paho.mqtt.client as mqtt
from loguru import logger
import playsound

"""THIS FILE RESIDES ON THE CLIENT AND MUST BE ACTIVE RUNNING PYTHON3 (NOT PYTHON2)"""

BROKER_HOST = "192.168.68.121"
BROKER_PORT = 1883
TOPIC_ON = "LIGHTSHOW_ON"
TOPIC_OFF = "LIGHTSHOW_OFF"
CLIENT_ID = None
QOS = 2

REGISTERED_KEYS = ("e", "f", "g", "a", "b", "c", "d", "k", "l")


class MusicController:

    is_down = False
    is_connect = False

    def __init__(self):
        pass

    def on_connect(self, client, userdata, flags, rc):
        self.is_connect = True
        logger.debug("Connected With Result Code: {}".format(rc))

    def send_publication(self, topic, payload):
        client = mqtt.Client(CLIENT_ID)
        client.on_connect = self.on_connect
        client.connect(BROKER_HOST, BROKER_PORT)
        payload = payload
        client.publish(topic, payload)

    def play_note_if_available(self, key):
        try:
            playsound.playsound('./notes/{0}3.mp3'.format(key), False)
        except playsound.PlaysoundException as err:
            pass

    def on_press(self, key):
        if not self.is_down:
            try:
                if "{0}".format(key.char) in REGISTERED_KEYS:
                    self.play_note_if_available(key.char)
                    self.send_publication(TOPIC_ON, "{0}".format(key.char))
                    self.is_down = True
                else:
                    # logger.warning("This press key is un-registered")
                    pass
            except AttributeError:
                pass
                # print('special key {0} pressed'.format(key))
        else:
            logger.debug("They are holding the key down.")

    def on_release(self, key):
        try:
            if "{0}".format(key.char) in REGISTERED_KEYS:
                self.send_publication(TOPIC_OFF, "{0}".format(key.char))
                self.is_down = False
            else:
                # logger.warning("This release key is un-registered")
                pass
        except AttributeError:
            pass
            # print('special key {0} pressed'.format(key))


if __name__ == "__main__":
    try:
        logger.info("JINGLE BELLS E E E - E E E - E G C D E - - -"
                    "F  F  F  F  F E E EE E D D E D "
                    "- G E E E - E E E - E G C D E - - - "
                    "F  F  F  F  F E E EE G G F D C")

        music_controller = MusicController()
        with keyboard.Listener(on_press=music_controller.on_press,
                               on_release=music_controller.on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        logger.info("Quiting Program")
