import logging
logger = logging.getLogger(__name__)
option = dict()

def config_setup():
    logger.debug("Starting config setup")
    file = open("settings.txt", "r")

    for line in file:
        temp = line.split(';')
        option[temp[0]] = temp[1]

def getValue(opti):
    return option.get(opti).rstrip("\n")
