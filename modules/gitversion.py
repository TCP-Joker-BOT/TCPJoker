import subprocess
import configreader


def run(_):
    configreader.ConfigReader('bot.cfg').set_command('id', 'id')
    return subprocess.check_output("git rev-parse HEAD".split(), universal_newlines=True)[0:7]
