"""
Summary:
~~~~~~~~
Returns current time.
"""
from datetime import datetime as dt


def run(_):
    return '{:02d} : {:02d}'.format(dt.now().hour, dt.now().minute)
