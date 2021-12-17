from os import name
from flask import Flask, render_template, redirect, request
import json

from werkzeug.wrappers import request
import music
import time
from loguru import logger
import click
from helpers import encode_json_for_mqtt

IS_DEBUG = True

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('home.html', name="Fun")

@app.route("/play/", methods=['POST'])
def play():
    dump(request.method)  
    return redirect("/")

@app.route("/dow/", methods=['GET', 'POST'])
def choose_loop(task=None):

    j = 'songs/journey.json'                  

    f = open(j)

    song = json.load(f)
    notes = song["notes"]
    loops = song["loops"]
    pause = song["pause"]

    logger.info(notes)

    music_controller = music.MusicController(notes, loops, False)

    # Always flash the lights off
    if not IS_DEBUG:
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
                logger.debug("note: ".format(note.lower()))
                if not IS_DEBUG:
                    # music_controller.play_note_if_available(note.lower())
                    # music_controller.send_publication(music.TOPIC_ON, encode_json_for_mqtt("{0}".format(note.lower()), float(pause)))
                    time.sleep(float(pause) * .45 + float(pause))
        # logger.warning("loop...")
        i = i + 1
    
    # Always end with the lights on
    if not IS_DEBUG:
        music_controller.send_publication(music.TOPIC_ON, encode_json_for_mqtt("1", pause))

    f.close()

    return "<p>Play Dow</p>" 