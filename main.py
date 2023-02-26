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
def main():
    config_setup()
    # test = testConnection(getValue("host"),getValue("port"),getValue("token"),getValue("org"),getValue("bucket"))
    # visuTimeseries(test)
    # data = solarTimePeriod(getValue("host"),getValue("port"),getValue("token"),getValue("org"),getValue("bucket"), datetime.datetime(2023,2,4,0,0,0), datetime.datetime(2023,2,5,0,0,0))
    # visuTimeseries(data)

    # series = loadDataDayScale(datetime.datetime(2023,2,4,0,0,0),23)
    seriesPowerMeter = loadDataPowerMeterDayScale(datetime.datetime(2023,2,25,0,0,0),2)
    for day in seriesPowerMeter:
        day.visualise()
        day.printStats()
    # solarStatistics(series,8)
main()
