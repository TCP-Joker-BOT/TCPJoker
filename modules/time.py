from datetime import datetime as dt


def run(_):
    return '{} : {}'.format(dt.now().hour, dt.now().minute)
