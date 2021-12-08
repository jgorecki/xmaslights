#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from loguru import logger
import sched
import _thread
import json

"""THIS FILE RESIDES ON THE PI AND MUST BE ACTIVE RUNNING PYTHON3 (NOT PYTHON2)"""

GPIO.setmode(GPIO.BCM)

BROKER_HOST = "raspberrypi.local"
BROKER_PORT = 1883
TOPIC_ON = "LIGHTSHOW_ON"
TOPIC_OFF = "LIGHTSHOW_OFF"
CLIENT_ID = None
QOS = 2
PIN_LIST = [26, 13, 22, 27, 6, 5, 0, 4]

REGISTERED_KEYS = (
    "e", "f", "g", "a", "b", "c", "d"  # these are the note keys
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"  # these are the flourish keys
)

SCHED = sched.scheduler(time.time, time.sleep)


def setup(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def cleanup():
    GPIO.cleanup()
    logger.debug("Cleaning up")


def powerup(pin, runtime):
    # logger.debug("pin: {0}".format(pin))
    powerdown(pin)
    GPIO.output(pin, GPIO.LOW)
    SCHED.enter(runtime, 1, powerdown, argument=[pin])


def powerdown(pin):
    # logger.debug("pin: {0}".format(pin))
    GPIO.output(pin, GPIO.HIGH)


def entry():
    for pin in PIN_LIST:
        setup(pin)


def on_connect(client, userdata, flags, rc):
    """
    I report that I've connected.  Its probably useful for updating UI?
    It returns zero upon success.
    """
    logger.debug("Connected With Result Code: {}".format(rc))


def press(x, runtime):
    """ Music keys """
    if x == "e":
        powerup(26, runtime)
    if x == "f":
        powerup(13, runtime)
    if x == "g":
        powerup(22, runtime)
    if x == "a":
        powerup(27, runtime)
    if x == "b":
        powerup(6, runtime)
    if x == "c":
        powerup(5, runtime)
    if x == "d":
        powerup(0, runtime)

    """ Flourish keys """
    # logger.debug(x)
    if x == "0":
        for pin in PIN_LIST:
            GPIO.output(pin, GPIO.HIGH)
    if x == "1":
        for pin in PIN_LIST:
            GPIO.output(pin, GPIO.LOW)
    if x == "2":
        powerup(26, runtime)
        powerup(13, runtime)
    if x == "3":
        powerup(13, runtime)
        powerup(22, runtime)
    if x == "4":
        powerup(27, runtime)
        powerup(6, runtime)
    if x == "5":
        powerup(6, runtime)
        powerup(5, runtime)
    if x == "6":
        powerup(5, runtime)
        powerup(0, runtime)
    if x == "7":
        powerup(26, runtime)
        powerup(13, runtime)
        powerup(22, runtime)
    if x == "8":
        powerup(27, runtime)
        powerup(6, runtime)
        powerup(5, runtime)
        powerup(0, runtime)
    if x == "9":
        powerup(26, runtime)
        powerup(22, runtime)
        powerup(6, runtime)
        powerup(5, runtime)

    _thread.start_new_thread(SCHED.run, ())


def on_message(client, userdata, message):
    """
    I've recieved a messaage from the broker.
    I can process said message here, maybe call a function, update some ui, send a request.
    """
    # logger.debug("Client got a message {}".format(message.payload.decode("utf-8")))

    # for pin in pinList:
    #     powerdown(pin)

    x = json.loads(message.payload.decode("utf-8"))
    logger.debug("json: {0}".format(x))
    t = message.topic

    if t == TOPIC_ON:
        press(x["key"], x["runtime"])


def main():

    entry()

    try:

        """Client Configuration."""
        client = mqtt.Client(CLIENT_ID)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER_HOST, BROKER_PORT)

        """Topic subscription. For multiples ... use a list of tuples [('topic', qs), (topic, qs)]"""
        client.subscribe([(TOPIC_ON, QOS), ])

        """Blocking loop."""
        client.loop_forever()

    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
