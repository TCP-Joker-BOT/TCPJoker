#!/usr/bin/python3

import sys
import json
import re
import urllib.request
import logger
import traceback
import os
import time
from configparser import ConfigParser


CONFIG_FILE_NAME = 'bot.cfg'
URL_BASE = 'https://api.telegram.org/bot'


def lock_wait(lock):
    if os.path.exists(lock):
        logger.info("\"Database\" is locked, waiting...")
        while os.path.exists(lock):
            time.sleep(1)
    open(lock, 'w').close()
    logger.info("Lock file created")


def lock_delete(lock):
    if os.path.exists(lock):
        try:
            os.remove(lock)
            logger.info("Finished, lock removed")
        except FileNotFoundError:
            logger.warn("Lock file not found")


def do_telegram_request(method, **data):
    config = ConfigParser(CONFIG_FILE_NAME)
    req = urllib.request.Request(URL_BASE + config.get_token() + '/' + method, headers={'Content-Type': 'application/json'})
    json_data = json.dumps(data)
    urllib.request.urlopen(req, json_data.encode('utf-8'))


def proceed_message(message_object):
    message_text = message_object['text']
    message_command = re.sub('^(.*?)[\\s@].*', '\\1', message_text)
    if message_command[0] != '/' or message_command == '':
        raise ValueError
    message_command = message_command[1:]
    logger.info('Command: ' + message_command)
    config = ConfigParser(CONFIG_FILE_NAME)
    module_name = config.get_command_dict()[message_command]
    logger.info('Command found in config')
    module = getattr(__import__('modules.' + module_name), module_name)  # Black python magic
    logger.info('Module successfully imported')
    lock_wait("users.lock")
    result = module.run(message_object)
    lock_delete("users.lock")
    return result


def send_answer(text, chat_id):
    logger.info('Sending answer: "' + text + '" to the chat ' + str(chat_id))
    do_telegram_request('sendMessage', chat_id=chat_id, text=text)


def main():
    logger.info('Got request')
    hook_data_raw = sys.stdin.read()
    hook_data = json.loads(hook_data_raw)
    update_id = hook_data['update_id']
    message_object = hook_data['message']
    answer = proceed_message(message_object)
    logger.info('Created answer: ' + answer)
    send_answer(answer, message_object['chat']['id'])


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.error(traceback.format_exc())
        logger.error('Incorrect exit')
