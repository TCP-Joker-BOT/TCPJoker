#!/usr/bin/env python3
import random
from urllib import request
import json
import logger
import users

#: Path to configuration file
CFG_PATH = "modules/joke.json"
#: Global variable to store module configuration
CONFIG = None
#: Default module configuration
DEFAULT_CONFIG = {
    "hivemind": False,
    "jokes": [
        "What's the best thing about having sex with twenty seven year olds?\n"
        "There are twenty of them!"
    ],
}


def load_config(path=None):
    """Loads config to :py:const:`CONFIG` from `CFG_PATH` or `path` if provided

    Args:
        path (string): path to the configuration file
    """

    global CONFIG

    path = path or CFG_PATH
    try:
        CONFIG = json.load(open(path, "r", encoding="utf-8"))
        logger.info("Loaded config")
    except FileNotFoundError:
        CONFIG = DEFAULT_CONFIG
        write_config(path=path)
        logger.info("Config not found, created default")


def write_config(data=None, path=None):
    """Writes :py:const:`CONFIG` or `CONFIG` (if provided) to `CFG_PATH` or `path` (if provided)

    Args:
        data: configuration data to serialize
        path (string): path to the configuration file
    """
    global CONFIG

    CONFIG = CONFIG or CONFIG
    path = path or CFG_PATH
    with open(path, "w", encoding="utf-8") as config:
        config.write(json.dumps(CONFIG))


def s_add(message):
    """Adds joke to joke pool if hivemind mode is on or joke sender is admin

    Args:
        message: Telegram message object
    Returns:
        str: result in human-readable format
    """
    logger.info("Add request...")
    joke = message['text'].split(' ', 2)[2]
    if CONFIG["hivemind"] or users.is_user_in_group(message["from"]["id"], 'joke') or users.is_user_admin(message["from"]["id"]):
        CONFIG["jokes"].append(joke)
        write_config(CONFIG)
        logger.info("Add request granted")
        return "Thx for your great joke!"
    else:
        logger.info("Add request denied")
        return "Sorry, adding jokes is enabled only for admins"


def s_search(message):
    """Searches joke pool case-insensitively.

    Args:
        message: Telegram message object
    Returns:
        str: seqrch results in human-readable format
    """
    logger.info("Search request...")
    try:
        query = message['text'].split(' ', 2)[2].lower()
    except IndexError:
        query = ""
    answer = ""
    ctr = 0
    for i in range(len(CONFIG["jokes"])):
        if query in CONFIG["jokes"][i].lower():
            ctr += 1
            answer = "{}{}: {}\n".format(answer, i, CONFIG["jokes"][i])
    logger.info("Found {} results, sending...".format(ctr))
    return answer.rstrip("\n") or "Sorry, I don't remember such a joke"


def s_delete(message):
    """Deletes joke from pool by number if sender is admin

    Args:
        message: Telegram message object
    Returns:
        str: result in human-readable format
    """
    logger.info("Deletion request...")
    if users.is_user_in_group(message["from"]["id"], 'joke') or users.is_user_admin(message["from"]["id"]):
        try:
            index = int(message['text'].split(' ', 2)[2])
            joke = CONFIG["jokes"].pop(index)
        except ValueError:
            logger.info("Invalid number")
            return "Hey, looks like NaN!"
        except IndexError:
            logger.info("Invalid number")
            return "I do not have SO many jokes yet"
        write_config(CONFIG)
        logger.info("Deletion request granted")
        return "Joke \"{}\" removed!".format(joke)
    else:
        return "Sorry, deleting jokes is only for admins"


def s_baneks(*_, recurse=1):
    """
    Returns random joke from `'B' category <https://vk.com/baneks>`_. Runs recursively until a joke with non-empty text is found.

    Args:
        recurse (Optional[int]): Depth of recursion. Defaults to 1.
    Returns:
        str: random joke from `'B' category <https://vk.com/baneks>`_
    """
    if recurse > 5:
        return "Sorry, an error occured"
    logger.info("Baneks request...")
    api = "https://api.vk.com/method/"
    rqst = request.urlopen(api + "wall.get?domain=baneks&count=1").read().decode()
    aneks_count = json.loads(rqst)["response"][0]
    rqst = request.urlopen(api + "wall.get?domain=baneks&offset={}&count=1".format(random.randint(1, aneks_count))).read().decode()
    return str(json.loads(rqst)["response"][1]["text"].replace("<br>", "\n")) or s_baneks(0, 0, 0, recurse=recurse + 1)


def s_hivemind(message):
    """Controls `hivemind` option state

    Args:
        message: Telegram message object
    Returns:
        str: result in human-readable format
    """
    if users.is_user_in_group(message["from"]["id"], 'joke') or users.is_user_admin(message["from"]["id"]):
        return "You haven't permission to do that"
    if message["text"].split(" ")[-1] == "on":
        CONFIG["hivemind"] = True
        write_config(CONFIG)
        return "Hivemind mode enabled"
    elif message["text"].split(" ")[-1] == "off":
        CONFIG["hivemind"] = False
        write_config(CONFIG)
        return "Hivemind mode disabled"
    elif message["text"].split(" ")[-1] == "hivemind":
        if CONFIG["hivemind"]:
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
        load_config()
    except:
        return "Sorry, an error occured"

    msg = message["text"].split(" ")
    if len(msg) > 1 and msg[1] in subcommands:
        return subcommands[msg[1]](message)
    else:
        logger.info("Joke request, replying")
        try:
            return random.choice(CONFIG["jokes"])
        except IndexError:
            return "Sorry, I don't have any jokes"
