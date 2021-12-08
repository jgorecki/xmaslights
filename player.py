import json
import music
import time
from loguru import logger
import click
from helpers import encode_json_for_mqtt

@click.command()
@click.option('--task', prompt='Choose a song to play: '
                               '0 {Jingle Bells}, '
                               '1 {Away in a manger}, '
                               '2 {We wish you a merry christmas}, '
                               'Choose an animation to play: '
                               'j {Joe}: '
                               'a {Alex}: '
                               'z {Zach}: '
                               'c {Colleen}: '
                               'd {Journey}: ')
def entry(task):

    j = 'songs/jinglebells.json'

    if task == "0":
        j = 'songs/jinglebells.json'

    elif task == "1":
        j = 'songs/awayinamanger.json'

    elif task == "2":
        j = 'songs/wewishyouamerrychristmas.json'

    elif task == "j":    
        j = 'animations/joe.json'

    elif task == "a":    
        j = 'animations/alex.json'

    elif task == "z":    
        j = 'animations/zach.json'

    elif task == "c":    
        j = 'animations/colleen.json'

    elif task == "d":    
        j = 'animations/journey.json'                        

    f = open(j)

    song = json.load(f)
    notes = song["notes"]
    loops = song["loops"]
    pause = song["pause"]

    logger.info(notes)

    music_controller = music.MusicController()

    # Always flash the lights off
    music_controller.send_publication(music.TOPIC_ON, encode_json_for_mqtt("0", pause))

    i = 0
    while i < loops:
        for note in notes:
            logger.debug(note)
            if note == ".":
                time.sleep(float(pause) * .45) # this is a delay
            if note == "-":
                time.sleep(float(pause)) # this is a pause
            else:
                music_controller.play_note_if_available(note.lower())
                music_controller.send_publication(music.TOPIC_ON, encode_json_for_mqtt("{0}".format(note.lower()), float(pause)))
                time.sleep(float(pause) * .45 + float(pause))
        # logger.warning("loop...")
        i = i + 1
    
    # Always end with the lights on
    music_controller.send_publication(music.TOPIC_ON, encode_json_for_mqtt("1", pause))

    f.close()


if __name__ == "__main__":
    entry()
