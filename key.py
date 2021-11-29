import paho.mqtt.client as mqtt
from loguru import logger
from pynput.keyboard import Key, Listener

# BROKER_HOST = "test.mosquitto.org"
BROKER_HOST = "192.168.68.121"
BROKER_PORT = 1883
TOPIC = "LIGHTSHOW"
CLIENT_ID = None
QOS = 2

def on_connect(client, userdata, flags, rc):
   """
   I report that I've connected.  Its not super userful for me right now in a cli.
   It returns zero upon success.
   """
   logger.debug("Connected With Result Code: {}".format(rc))


def send_publication(payload):

   logger.debug("Sending...")

   """Client Config"""
   client = mqtt.Client(CLIENT_ID)
   client.on_connect = on_connect
   client.connect(BROKER_HOST, BROKER_PORT)

   """Topic (key)"""
   topic = TOPIC

   """Payload for the topic (value, text, etc)"""
   payload = payload

   """Topic subscription."""
   client.publish(topic, payload)

def show(key):
   # logger.debug(key)
   keys = ("'a'", "'s'", "'d'", "'f'", "'g'", "'h'", "'j'", "'k'")

   if "{0}".format(key) in keys:
      send_publication("{0}".format(key))
   else:
      logger.warning("This key is un-registered")

    # if key == Key.tab:
    #     return False

# Collect all event until released
with Listener(on_press=show) as listener:
    listener.join()

