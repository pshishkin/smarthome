import time
import subprocess
import telegram
import traceback
import logging

bot = telegram.Bot(token='204250979:AAHXHHLeckrvG9elzP8AyFo-5VTSGx_s2tY')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def is_free_slots(curl_line):
    downloaded_data = subprocess.check_output(curl_line.strip() + ' -s', shell=True, universal_newlines=True)
    return 'data-time' in downloaded_data


with open('curl_lines.txt') as infile:
    curl_lines_check = infile.readlines()

with open('curl_lines_should_be.txt') as infile:
    curl_lines_should_be = infile.readlines()



while True:
    logging.info('Checking doctors')

    for curl_line in curl_lines_check:
        try:
            if is_free_slots(curl_line):
                bot.sendMessage(chat_id=-124691948, text='Hey, there is free doctor!')
                logging.info('Hey, there is free doctor!')
        except:
            traceback.print_exc()

    for curl_line in curl_lines_should_be:
        fail = False
        try:
            if not is_free_slots(curl_line):
                fail = True
                bot.sendMessage(chat_id=-124691948, text='Hey, I cant found free space in free doctor schedule, Im exiting!')
                logging.info('Hey, I cant found free space in free doctor schedule, Im exiting!')
        except:
            traceback.print_exc()
        if fail:
            exit(-1)

    time.sleep(5*60)

