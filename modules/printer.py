import re


def run(message):
    text = message['text']
    command = re.sub('^(.*?)[\\s@].*$', '\\1', text)
    if command[0] != '/':
        raise ValueError
    filename = 'printer_data/' + command[1:] + '.txt'
    f = open(filename, 'r')
    result = f.read()
    f.close()
    return result
