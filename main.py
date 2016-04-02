#!/usr/bin/python3

import sys
import json
import re
import urllib.request
from configparser import ConfigParser


CONFIG_FILE_NAME = 'bot.cfg'
URL_BASE = 'https://api.telegram.org/bot'


def do_telegram_request(method, **data):
    config = ConfigParser(CONFIG_FILE_NAME)
    req = urllib.request.Request(URL_BASE + config.get_token() + '/' + message + '/' + method, headers={'Content-Type': 'application/json'})
    json_data = json.dumps(data)
    urllib.request.urlopen(req, json_data.encode('utf-8'))

def proceed_message(message_object):
    message_text = message_object['text']
    message_command = re.sub('^(.*?)[\\s@].*', '\\1', message_text)
    if message_command[0] != '/' or message_command == '':
        raise ValueError
    message_command = message_command[1:]
    config = ConfigParser(CONFIG_FILE_NAME)
    module_name = config.get_command_dict()[message_command]
    module = __import__(module_name)
    return module.run(message_object)

def send_answer(text, chat_id):
    do_telegram_request('sendMessage', chat_id=chat_id, text=text)

def main():
    hook_data_raw = sys.stdin.read()
    hook_data = json.loads(hook_data_raw)
    update_id = hook_data['update_id']
    message_object = hook_data['message']
    answer = proceed_message(message_object) 
    send_answer(answer, message_object['chat'])

if __name__ == '__main__':
    main()

