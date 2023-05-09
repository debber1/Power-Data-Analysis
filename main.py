from config import *
from db import *
from visualise import *
from util import *
from load import *
from analysis import *
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import timePeriod
import os
import logging
import sys

from colargulog import ColorizedArgsFormatter
from colargulog import BraceFormatStyleFormatter


def init_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)


    console_level = "DEBUG"
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(console_level)
    console_format = "%(asctime)s - %(levelname)-8s - %(name)-25s - %(message)s"
    colored_formatter = ColorizedArgsFormatter(console_format)
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)

    file_handler = logging.FileHandler("app.log")
    file_level = "DEBUG"
    file_handler.setLevel(file_level)
    file_format = "%(asctime)s - %(name)s (%(lineno)s) - %(levelname)-8s - %(threadName)-12s - %(message)s"
    file_handler.setFormatter(BraceFormatStyleFormatter(file_format))
    root_logger.addHandler(file_handler)


init_logging()
logger = logging.getLogger(__name__)

def main():
    logger.info("Loading setup")
    config_setup()
    # test = testConnection(getValue("host"),getValue("port"),getValue("token"),getValue("org"),getValue("bucket"))
    # visuTimeseries(test)
    # data = solarTimePeriod(getValue("host"),getValue("port"),getValue("token"),getValue("org"),getValue("bucket"), datetime.datetime(2023,2,4,0,0,0), datetime.datetime(2023,2,5,0,0,0))
    # visuTimeseries(data)
    save = False
    if(save):
        logger.info("Saving is on")
    else:
        logger.info("Saving is off")
    startDay = str(localToUtc(datetime.datetime.now(timezone.utc)))

    # series = loadDataDayScale(datetime.datetime(2023,2,4,0,0,0),23)
    logger.info("Starting loading of the data")
    seriesPowerMeter = loadDataDayScale(localToUtc(datetime.datetime(2023,2,25,0,0,0)),66)
    logger.info("Finished loading of the data")


    #seriesPowerMeter[1].visualisePower()
    #seriesPowerMeter[1].visualise()
    #for day in seriesPowerMeter:
    #    day.visualise()
    #    day.printStats()
    if(save):
        os.mkdir(startDay)
    solarStatistics(seriesPowerMeter,8, save, startDay + "/")
    powerStatistics(seriesPowerMeter,8, save, startDay + "/")

main()
