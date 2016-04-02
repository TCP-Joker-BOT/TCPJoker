LOG_NAME = 'bot.log'
LOG_FILE = open(LOG_NAME, 'a')

def info(message):
    print('[INFO] ' + message, file=LOG_FILE)

def warning(message):
    print('[WARN] ' + message, file=LOG_FILE)

def error(message):
    print('[ERR!] ' + message, file=LOG_FILE)

