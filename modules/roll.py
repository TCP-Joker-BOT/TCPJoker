#!/usr/bin/python3
import random

def run(message):
    args = message['text'].slpit()[1:]
    if len(args) == 0:
        return str(random.randint(1, 6))
    elif len(args) == 1 and args[0].isdigit():
        return str(random.randint(1, int(args[0])))
    return 'Incorrect syntax, see /help for help'
