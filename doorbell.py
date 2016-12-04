import RPi.GPIO as GPIO
import signal
from time import sleep
import urllib
import urllib2
import datetime
import logging

SECONDS_BETWEEN_BELLS = 20
DOOR_BELL_PIN = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(DOOR_BELL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

last_press = datetime.datetime.now()

def check_pin_n_times(pin, times, timeout):
    for try_num in xrange(times):
        if GPIO.input(pin) != GPIO.HIGH:
            return False
        sleep(timeout)
    return True

def button_pressed(channel):
    global last_press
    if (datetime.datetime.now() - last_press).total_seconds() < SECONDS_BETWEEN_BELLS:
        return
    logging.info('Seems that button is pressed')
    if check_pin_n_times(DOOR_BELL_PIN, 3, 0.001):
        logging.info('Button is really pressed')
        last_press = datetime.datetime.now()
        data = ''
        req = urllib2.Request('https://hooks.zapier.com/hooks/catch/994827/2tgm4j//?type=dong', data)
        response = urllib2.urlopen(req)
        the_page = response.read()
    else:
        logging.info('No, button isnt pressed')


def cleanup(_signo, _stack_frame):
    print("Cleaning up")
    GPIO.cleanup()
    exit(0)


GPIO.add_event_detect(DOOR_BELL_PIN, GPIO.RISING, callback=button_pressed, bouncetime=1)
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG)

logging.info('Doorbell started')

while True:
    sleep(1)
