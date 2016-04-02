#!/usr/bin/env python3
import random
import sys
import os
sys.path.append(os.getcwd())  # HACK, surly we don't want to write modules like this
import json
import logger
import traceback


def run(message):
    try:
        data = json.load(open("modules/joke.json", "r", encoding="utf-8"))
        logger.info("Loaded config")
    except FileNotFoundError:
        with open("modules/joke.json", "w", encoding="utf-8") as fl:
            data = {
                "hivemind": False,
                "admins": [
                    74741895,
                    187843269
                ],
                "jokes": [
                    "What's the best thing about having sex with twenty seven year olds?\n"
                    "There are twenty of them!"
                ]
            }
            fl.write(json.dumps(data))
        logger.info("Config not found, created default")
    except:
        logger.error("Uncaught error:")
        logger.error(traceback.format_exc())
        return "Sorry, an error occured"

    msg = message["text"].split(" ")
    if len(msg) > 1:
        if msg[1] == "add":
            logger.info("Add request...")
            if (data["hivemind"] or message["from"]["id"] in data["admins"]):
                data["jokes"].append(" ".join(msg[2:]))
                with open("modules/joke.json", "w", encoding="utf-8") as fl:
                    fl.write(json.dumps(data))
                logger.info("Add request granted")
                return "Thx for your great joke!"
            else:
                logger.info("Add request denied")
                return "Sorry, adding jokes is enabled only for admins"
        elif msg[1] == "somesubcommand":
            pass  # WIP
        else:
            logger.info("Unknown subcommand, ignoring")
            return random.choice(data["jokes"])
    else:
        logger.info("Joke request, replying")
        return random.choice(data["jokes"])
