#!/usr/bin/env python3
import random
from urllib import request
import json
import logger
import users

CFG_PATH = "modules/joke.json"


def load_config():
    try:
        data = json.load(open(CFG_PATH, "r", encoding="utf-8"))
        logger.info("Loaded config")
    except FileNotFoundError:
        write_config(
            {
                "hivemind": False,
                "admins": [
                    74741895,
                    187843269
                ],
                "jokes": [
                    "What's the best thing about having sex with twenty seven year olds?\n"
                    "There are twenty of them!"
                ],
            })
        logger.info("Config not found, created default")
    return data


def write_config(data):
    with open(CFG_PATH, "w", encoding="utf-8") as config:
        config.write(json.dumps(data))


def s_add(data, joke, message):
    logger.info("Add request...")
    if (data["hivemind"] or users.is_user_admin(message["from"]["id"])):
        data["jokes"].append(joke)
        write_config(data)
        logger.info("Add request granted")
        return "Thx for your great joke!"
    else:
        logger.info("Add request denied")
        return "Sorry, adding jokes is enabled only for admins"


def s_search(data, query, _):
    logger.info("Search request...")
    query = query.lower()
    answer = ""
    ctr = 0
    for i in range(len(data["jokes"])):
        if query in data["jokes"][i].lower():
            ctr += 1
            answer = "{}{}: {}\n".format(answer, i, data["jokes"][i])
    logger.info("Found {} results, sending...".format(ctr))
    return answer.rstrip("\n") or "Sorry, I don't remember such a joke"
    # crazy pythonista way
    # return "\n".join([str(data["jokes"].index(s)) + ": " + s for s in data["jokes"] if " ".join(msg[2:]).lower() in s.lower()])


def s_delete(data, index, message):
    logger.info("Deletion request...")
    if users.is_user_admin(message["from"]["id"]):
        try:
            index = int(index)
            joke = data["jokes"].pop(index)
        except ValueError:
            logger.info("Invalid number")
            return "Hey, looks like NaN!"
        except IndexError:
            logger.info("Invalid number")
            return "I do not have SO many jokes yet"
        write_config(data)
        logger.info("Deletion request granted")
        return "Joke \"{}\" removed!".format(joke)
    else:
        return "Sorry, deleting jokes is only for admins"


def s_baneks(_, __, ___, recurse=1):
    if recurse > 5:
        return "Sorry, an error occured"
    logger.info("Baneks request...")
    api = "https://api.vk.com/method/"
    rqst = request.urlopen(api + "wall.get?domain=baneks&count=1").read().decode()
    aneks_count = json.loads(rqst)["response"][0]
    rqst = request.urlopen(api + "wall.get?domain=baneks&offset={}&count=1".format(random.randint(1, aneks_count))).read().decode()
    return str(json.loads(rqst)["response"][1]["text"].replace("<br>", "\n")) or s_baneks(0, 0, 0, recurse=recurse + 1)


def s_hivemind(data, __, message):
    if message["from"]["id"] not in data["admins"]:
        return "You haven't permission to do that"
    if message["text"].split(" ")[-1] == "on":
        data["hivemind"] = True
        write_config(data)
        return "Hivemind mode enabled"
    elif message["text"].split(" ")[-1] == "off":
        data["hivemind"] = False
        write_config(data)
        return "Hivemind mode disabled"
    elif message["text"].split(" ")[-1] == "hivemind":
        if data["hivemind"]:
            return "Hivemind is enabled now"
        else:
            return "Hivemind is disabled now"
    else:
        return "Unknown hivemind state"


def run(message):
    subcommands = {
        "add": s_add,
        "search": s_search,
        "delete": s_delete,
        "baneks": s_baneks,
        "hivemind": s_hivemind
    }
    try:
        data = load_config()
    except:
        return "Sorry, an error occured"

    msg = message["text"].split(" ")
    if len(msg) > 1 and msg[1] in subcommands:
        return subcommands[msg[1]](data, " ".join(msg[2:]), message)
    else:
        logger.info("Joke request, replying")
        return random.choice(data["jokes"])
