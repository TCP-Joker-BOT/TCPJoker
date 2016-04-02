#!/usr/bin/env python
import random
import json
import os


def run(message):
    try:
        data = json.load(open("modules/joke.json", "r"))
    except FileNotFoundError:
        with open("joke.json", "w") as fl:
            data = {
                "hivemind": False,
                "admins": [
                    74741895,
                ],
                "jokes": [
                    "Q: What did one lesbian vampire say to the other one?\n"
                    "A: See ya next month.",
                ]
            }
            fl.write(json.dumps(data))
    except json.decoder.JSONDecodeError:
        raise Exception("Jokes database seems to be corrupted")
    msg = message["text"].split(" ")
    if len(msg) > 1:
        if msg[1] == "add":
            if (data["hivemind"] or message["from"]["id"] in data["admins"]):
                data["jokes"].append(" ".join(msg[2:]))
                with open("joke.json", "w") as fl:
                    fl.write(json.dumps(data))
                return "Thx for your great joke!"
            else:
                return "Sorry, adding jokes is enabled only for admins"
        elif msg[1] == "somesubcommand":
            pass  # WIP
        else:
            return random.choice(data["jokes"])
    else:
        return random.choice(data["jokes"])
