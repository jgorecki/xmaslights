from pynput import keyboard
import paho.mqtt.client as mqtt
from loguru import logger
import playsound
import json
import time
import click
from helpers import encode_json_for_mqtt
from random import randint


"""THIS FILE RESIDES ON THE CLIENT AND MUST BE ACTIVE RUNNING PYTHON3 (NOT PYTHON2)"""

BROKER_HOST = "192.168.68.121"
# BROKER_HOST = "raspberrypi.local"
BROKER_PORT = 1883
TOPIC_ON = "LIGHTSHOW_ON"
TOPIC_OFF = "LIGHTSHOW_OFF" # This is unused.
CLIENT_ID = None
QOS = 2
PAUSE = .45

REGISTERED_KEYS = (
    "e", "f", "g", "a", "b", "c", "d",  # these are the note keys
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",  # these are the flourish keys
    ".", "-"
)

class MusicController:

    is_down = False
    is_connect = False
    is_game = False

    song_notes = []
    user_notes = []

    def __init__(self, song_notes, song_loops, is_game):
        self.song_notes = song_notes
        self.song_loops = song_loops
        self.is_game = is_game

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

    def gamify(self, key):

        if len(self.user_notes) == len(self.song_notes):
            score = sum(1 for x, y in zip(self.song_notes, self.user_notes) if x == y) / len(self.song_notes)
            print("")
            print("COMPLETE!")
            print("")
            print("You're final score is: {0}!".format(score))
            print("-" * 1000)
            print("")
            time.sleep(3)
            raise KeyboardInterrupt
        else:
            self.user_notes.append(key)

    def on_press(self, key):
        if not self.is_down:
            try:
                if self.is_game:
                    self.gamify(key.char.upper()) # save the down pressed keu to the user's key presses
                if "{0}".format(key.char) in REGISTERED_KEYS:
                    self.play_note_if_available(key.char)
                    self.send_publication(TOPIC_ON, encode_json_for_mqtt("{0}".format(key.char), PAUSE))
                    self.is_down = True
                else:
                    # logger.info("This press key is un-registered")
                    pass
            except AttributeError:
                # logger.warning('special key {0} pressed'.format(key))
                pass
        else:
            # logger.warning("They are holding the key down.")
            pass

    def on_release(self, key):
        try:
            if "{0}".format(key.char) in REGISTERED_KEYS:
                # self.send_publication(TOPIC_OFF, "{0}".format(key.char))
                self.is_down = False
            else:
                # logger.warning("This release key is un-registered")
                pass
        except AttributeError:
            pass
            # print('special key {0} pressed'.format(key))


@click.command()
@click.option('--task', prompt='Choose a song to play: '
                               '0 {Jingle Bells}, '
                               '1 {Away in a manger}, '
                               '2 {We wish you a merry christmas}'
)

def entry(task):

    try:

        j = 'songs/jinglebells.json'

        is_game = True

        if task == "0":
            j = 'songs/jinglebells.json'

        elif task == "1":
            j = 'songs/awayinamanger.json'

        elif task == "2":
            j = 'songs/wewishyouamerrychristmas.json'
        
        elif task == "777":
            j = 'songs/test.json'                       
            
        f = open(j)

        song = json.load(f)
        notes = song["notes"]
        loops = song["loops"]

        print("Hi.  You'll be playing {0} loops of this song. '.' and '-' count.".format(loops))
        print(notes)

        music_controller = MusicController(notes, loops, is_game)
        with keyboard.Listener(on_press=music_controller.on_press,
                               on_release=music_controller.on_release) as listener:
            listener.join()
    except KeyboardInterrupt:
        logger.info("Quiting Program")

if __name__ == "__main__":
    entry()
