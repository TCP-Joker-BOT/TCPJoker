from datetime import datetime as dt


LOG_NAME = 'bot.log'
LOG_FILE = open(LOG_NAME, 'a', encoding='utf-8')


def curr_time():
    return '{:02d}:{:02d}:{:02d}'.format(dt.now().hour, dt.now().minute, dt.now().second)


def info(message):
    print(curr_time() + ' [INFO] ' + message, file=LOG_FILE)


def warning(message):
    print(curr_time() + ' [WARN] ' + message, file=LOG_FILE)


def error(message):
    print(curr_time() + ' [ERR!] ' + message, file=LOG_FILE)
