import json
import music
import time
from loguru import logger
import click

@click.command()
@click.option('--task', prompt='Choose ta song to play: '
                               '0 {Jingle Bells}, '
                               '1 {Away in a manger}, '
                               '2 {We wish you a merry christmas}, ')
def entry(task):

    j = 'songs/jinglebells.json'

    if int(task) == 0:
        j = 'songs/jinglebells.json'

    elif int(task) == 1:
        j = 'songs/awayinamanger.json'

    elif int(task) == 2:
        j = 'songs/wewishyouamerrychristmas.json'

    f = open(j)

    song = json.load(f)
    notes = song["notes"]
    loops = song["loops"]
    pause = song["pause"]

    music_controller = music.MusicController()

    i = 0
    while i < loops:
        for note in notes:
            # logger.debug(note)
            music_controller.play_note_if_available(note.lower())
            music_controller.send_publication(music.TOPIC_ON, "{0}".format(note.lower()))
            time.sleep(pause * .45)
        # logger.warning("loop...")
        i = i + 1

    f.close()


if __name__ == "__main__":
    entry()
