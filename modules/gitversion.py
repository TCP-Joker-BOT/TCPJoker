import subprocess


def run(_):
    return subprocess.check_output("git rev-parse HEAD".split(), universal_newlines=True)[0:7]
