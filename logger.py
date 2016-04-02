from datetime import datetime as dt


LOG_NAME = 'bot.log'
LOG_FILE = open(LOG_NAME, 'a')


def curr_time():
    return '{}:{}:{}'.format(dt.now().hour, dt.now().minute, dt.now().second)


def info(message):
    print(curr_time() + ' [INFO] ' + message, file=LOG_FILE)


def warning(message):
    print(curr_time() + ' [WARN] ' + message, file=LOG_FILE)


def error(message):
    print(curr_time() + ' [ERR!] ' + message, file=LOG_FILE)
