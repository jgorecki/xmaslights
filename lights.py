#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pause = 1
pinList = [26, 13, 22, 27, 6, 5, 22, 27, 0, 4]
# pinList = [26, 13, 4, 0, 13, 4, 0, 0, 4, 13, 26, 4, 0, 4, 0, 4, 0]

# loop through pins and set mode and state to 'low'
def setup(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def cleanup():
    GPIO.cleanup()
    print("cleanup")


def powerup(pin):
    print("pin: {0}".format(pin))
    # if pin == 0:
    #     cleanup()
    #     entry()
    #     return
    GPIO.output(pin, GPIO.LOW)

def entry():
    for pin in pinList:
        setup(pin)

def main():

    entry()

    try:
        i = 0
        for pin in pinList:
            powerup(pin)
            i = i + 1
            time.sleep(pause)
            if i == len(pinList):
                time.sleep(5)
                cleanup()

    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
