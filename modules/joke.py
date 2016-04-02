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
        elif msg[1] == "search":
            logger.info("Search request...")
            sub = " ".join(msg[2:])
            answer = ""
            ctr = 0
            for i in range(len(data["jokes"])):
                if sub.lower() in data["jokes"][i].lower():
                    ctr += 1
                    answer = "{}{}: {}\n".format(answer, i, data["jokes"][i])
            logger.info("Found {} results, sending...".format(ctr))
            return answer.rstrip("\n")
            # crazy pythonista way
            # return "\n".join([str(data["jokes"].index(s)) + ": " + s for s in data["jokes"] if " ".join(msg[2:]).lower() in s.lower()])
        elif msg[1] == "delete":
            logger.info("Deletion request...")
            if message["from"]["id"] in data["admins"]:
                try:
                    index = int(" ".join(msg[2:]))
                    joke = data["jokes"].pop(index)
                except ValueError:
                    logger.info("Invalid number")
                    return "Hey, looks like NaN!"
                except IndexError:
                    logger.info("Invalid number")
                    return "I do not have SO many jokes yet"
                with open("modules/joke.json", "w", encoding="utf-8") as fl:
                    fl.write(json.dumps(data))
                logger.info("Deletion request granted")
                return "Joke \"{}\" removed!".format(joke)
            else:
                return "Sorry, deleting jokes is only for admins"

        else:
            logger.info("Unknown subcommand, ignoring")
            return random.choice(data["jokes"])
    else:
        logger.info("Joke request, replying")
        return random.choice(data["jokes"])
