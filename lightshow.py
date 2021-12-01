#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from loguru import logger
import sched
import _thread

"""THIS FILE RESIDES ON THE PI AND MUST BE ACTIVE RUNNING PYTHON3 (NOT PYTHON2)"""

GPIO.setmode(GPIO.BCM)

# BROKER_HOST = "test.mosquitto.org"
BROKER_HOST = "192.168.68.121"
BROKER_PORT = 1883
TOPIC_ON = "LIGHTSHOW_ON"
TOPIC_OFF = "LIGHTSHOW_OFF"
CLIENT_ID = None
QOS = 2

PAUSE = .45
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


def powerup(pin):
    # logger.debug("pin: {0}".format(pin))
    powerdown(pin)
    GPIO.output(pin, GPIO.LOW)
    SCHED.enter(PAUSE, 1, powerdown, argument=[pin])


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


def press(x):
    """ Music keys """
    if x == "e":
        powerup(26)
    if x == "f":
        powerup(13)
    if x == "g":
        powerup(22)
    if x == "a":
        powerup(27)
    if x == "b":
        powerup(6)
    if x == "c":
        powerup(5)
    if x == "d":
        powerup(0)

    """ Flourish keys """
    # logger.debug(x)
    if x == "0":
        for pin in PIN_LIST:
            GPIO.output(pin, GPIO.HIGH)
    if x == "1":
        for pin in PIN_LIST:
            GPIO.output(pin, GPIO.LOW)
    if x == "2":
        powerup(26)
        powerup(13)
    if x == "3":
        powerup(13)
        powerup(22)
    if x == "4":
        powerup(27)
        powerup(6)
    if x == "5":
        powerup(6)
        powerup(5)
    if x == "6":
        powerup(5)
        powerup(0)
    if x == "7":
        powerup(26)
        powerup(13)
        powerup(22)
    if x == "8":
        powerup(27)
        powerup(6)
        powerup(5)
        powerup(0)
    if x == "9":
        powerup(26)
        powerup(22)
        powerup(6)
        powerup(5)

    _thread.start_new_thread(SCHED.run, ())


def on_message(client, userdata, message):
    """
    I've recieved a messaage from the broker.
    I can process said message here, maybe call a function, update some ui, send a request.
    """
    # logger.debug("Client got a message {}".format(message.payload.decode("utf-8")))

    # for pin in pinList:
    #     powerdown(pin)

    x = message.payload.decode("utf-8")
    t = message.topic

    if t == TOPIC_ON:
        press(x)


def main():

    entry()

    try:

        """Client Configuration."""
        client = mqtt.Client(CLIENT_ID)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER_HOST, BROKER_PORT)

        """Topic subscription. For multiples ... use a list of tuples [('topic', qs), (topic, qs)]"""
        client.subscribe([(TOPIC_ON, 2), (TOPIC_OFF, 2)])

        """Blocking loop."""
        client.loop_forever()

    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
