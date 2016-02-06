import RPi.GPIO as GPIO
import signal
from time import sleep
import urllib
import urllib2

SECONDS_BETWEEN_BELLS = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def button_pressed(channel):
    print("Button pressed!")
    data = ''
    req = urllib2.Request('https://zapier.com/hooks/catch/2tgm4j/?type=dong', data)
    response = urllib2.urlopen(req)
    the_page = response.read()

def cleanup(_signo, _stack_frame):
    print("Cleaning up")
    GPIO.cleanup()
    exit(0)

GPIO.add_event_detect(7, GPIO.RISING, callback=button_pressed, bouncetime=1000*SECONDS_BETWEEN_BELLS)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

while True:
    sleep(1)