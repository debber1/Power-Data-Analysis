from timePeriod import *
from util import *
from visualise import *
from datetime import datetime
import math
import multiprocessing
import logging
logger = logging.getLogger(__name__)
def solarAnalysis(periods, PID, returns):
    """
    This function performs an analysis over multiple timeperiods

    :param periods: List of timePeriodData: a list of time period data
    """
    logger.info("Starting statistics")
    # Extracting key statistics
    time = []
    totalPower = []
    activeTime = []
    mostIntensiveInterval = []
    mostIntensiveIntervalPower = []
    for period in periods:
        time.append(period.periodStart)
        temp = period.statistics()
        totalPower.append(temp["Total power"])
        activeTime.append(temp["Active time"])
        mostIntensiveInterval.append(temp["Most intensive interval"][0])
        mostIntensiveIntervalPower.append(temp["Most intensive interval"][1])

    returns[PID] = [time, totalPower, activeTime, mostIntensiveInterval, mostIntensiveIntervalPower]

def powerAnalysis(periods, PID, returns):
    """
    This function performs an analysis over multiple timeperiods

    :param periods: List of timePeriodData: a list of time period data
    """
    logger.info("Starting statistics")
    # Extracting key statistics
    time = []
    mostIntensiveInterval = []
    mostIntensiveIntervalPower = []
    for period in periods:
        time.append(period.periodStart)
        temp = period.statistics()
        mostIntensiveInterval.append(temp["Most intensive interval power"][0])
        mostIntensiveIntervalPower.append(temp["Most intensive interval power"][1])

    returns[PID] = [time, mostIntensiveInterval, mostIntensiveIntervalPower]



def showGeneratedData(firstPeriod, time, totalPower, activeTime, mostIntensiveInterval, mostIntensiveIntervalPower, save=False, savePath = "./"):

    barPlotTimeSeries(mergeTimeSeries(time,totalPower), "SOLAR: Total power generation per day", 0.5, save, savePath)

    barPlotTimeSeries(mergeTimeSeries(time, activeTime), "SOLAR: Total active hours per day", 0.5, save, savePath)

    barPlotTimeSeries(mergeTimeSeries(time, mostIntensiveIntervalPower), "SOLAR: Most intensive interval average power per day", 0.5, save, savePath)

    barPlotDayOverview(periodOverviewList(firstPeriod.periodStart, firstPeriod.periodEnd, mostIntensiveInterval), "SOLAR: Overview of peak average periods", 0.9, save, savePath)

def showGeneratedPowerData(firstPeriod, time, mostIntensiveInterval, mostIntensiveIntervalPower, save=False, savePath = "./"):

    barPlotTimeSeries(mergeTimeSeries(time, mostIntensiveIntervalPower), "POWER: Most intensive interval average power usage per day", 0.5, save, savePath)

    barPlotDayOverview(periodOverviewList(firstPeriod.periodStart, firstPeriod.periodEnd, mostIntensiveInterval), "POWER: Overview of peak average usage periods", 0.9, save, savePath)

def solarStatistics(periods, threads, save = False, savePath = "./"):
    """
    This function performs an analysis over multiple timeperiods

    :param periods: List of timePeriodData: a list of time period data
    """
    time = []
    totalPower = []
    activeTime = []
    mostIntensiveInterval = []
    mostIntensiveIntervalPower = []
    startTime = datetime.now()
    threadslist = []
    devisions = int(math.floor(len(periods)/threads))
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    for x in range(threads-1):
        threadslist.append(multiprocessing.Process(target = solarAnalysis, args= (periods[(x*devisions):((x+1)*devisions)],x, return_dict)))
        pass
    threadslist.append(multiprocessing.Process(target = solarAnalysis, args= (periods[devisions*(threads-1):],threads, return_dict)))
    for y in threadslist:
        y.start()
    for y in threadslist:
        y.join()
    for y in range(threads):
        results = return_dict.values()[y]
        time += results[0]
        totalPower += results[1]
        activeTime += results[2]
        mostIntensiveInterval += results[3]
        mostIntensiveIntervalPower += results[4]
    endTime = datetime.now()
    logger.info("It took "+ str((endTime-startTime).total_seconds())+" seconds to perform statistics on the data")
    showGeneratedData(periods[0], time, totalPower, activeTime, mostIntensiveInterval, mostIntensiveIntervalPower, save, savePath)


class myThread:
   def __init__(self, data):
        self.value = None
        self.data = data
   def run(self):
        self.value = solarAnalysis(self.data)

def powerStatistics(periods, threads, save = False, savePath = "./"):
    """
    This function performs an analysis over multiple timeperiods

    :param periods: List of timePeriodData: a list of time period data
    """
    time = []
    mostIntensiveInterval = []
    mostIntensiveIntervalPower = []
    startTime = datetime.now()
    threadslist = []
    devisions = int(math.floor(len(periods)/threads))
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    for x in range(threads-1):
        threadslist.append(multiprocessing.Process(target = powerAnalysis, args= (periods[(x*devisions):((x+1)*devisions)],x, return_dict)))
        pass
    threadslist.append(multiprocessing.Process(target = powerAnalysis, args= (periods[devisions*(threads-1):],threads, return_dict)))
    for y in threadslist:
        y.start()
    for y in threadslist:
        y.join()
    for y in range(threads):
        results = return_dict.values()[y]
        time += results[0]
        mostIntensiveInterval += results[1]
        mostIntensiveIntervalPower += results[2]
    endTime = datetime.now()
    logger.info("It took "+ str((endTime-startTime).total_seconds())+" seconds to perform statistics on the data")
    showGeneratedPowerData(periods[0], time, mostIntensiveInterval, mostIntensiveIntervalPower, save, savePath)
