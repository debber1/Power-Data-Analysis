from datetime import datetime, timezone, timedelta
from config import *
import pandas as pd
import logging
logger = logging.getLogger(__name__)

def utcToLocal(date):
    return date.replace(tzinfo=timezone.utc).astimezone(tz=None)

def localToUtc(date):
    return date.replace(tzinfo=None).astimezone(tz=timezone.utc)

def integralTimeSeries(data):
    """
    This function calculates the discrete integral of a timeseries while taking real life limitations into account (such as reporting at the beginning and ending of a solar cycle)

    :param data: List of List: A list with lists containing data points: [[time, data], [time, data]]
    :return: Int: total power used/produced over the timeperiod
    """
    logger.debug("Running integralTimeSeries")
    pil = []
    dtl = []
    for pair in range(len(data)-1):
        #Extract 2 datapoints
        data1 = data[pair]
        data2 = data[pair+1]

        # If one of the two datapoints is equal to zero, reject the calculation
        if data1[1] == 0 or data2[1] == 0:
            continue
        

        # Calculate the time difference between them in hours
        dt = (data2[0]-data1[0]).total_seconds()/3600

        # Calculate the difference in absolute value between the two points
        dp = data2[1] - data1[1]

        # Calculate the average power over dt
        pi = data1[1] + dp/2

        # Add the calculation to the lists
        pil.append(pi)
        dtl.append(dt)
    
    # Calculate the discrete integral with pi*dt
    power = 0
    for i in range(len(dtl)):
        power += dtl[i]*pil[i]

    return power

def activeTime(data):
    """
    This function calculates the amount of time a device was active based on power usage

    :param data: List of List: A list with lists containing data points: [[time, data], [time, data]]
    :return: Int: Total amount of hours a device has been active
    """
    logger.debug("Running activeTime")
    total = 0
    for pair in range(len(data)-1):
        #Extract 2 datapoints
        data1 = data[pair]
        data2 = data[pair+1]

        # If one of the two datapoints is equal to zero, reject the calculation
        if data1[1] == 0 or data2[1] == 0:
            continue
        
        # Calculate the time difference between them in hours and add it to the total
        total += (data2[0]-data1[0]).total_seconds()/3600
    
    return total

def rebaseTimeSeriesSolar(data):
    """
    This function rebases a time series to a common base to enable proper comparisons between datasets

    :param data: List of List: A list with lists containing data points: [[time, data], [time, data]]
    :return: List of List: A list with lists containing data points: [[time, data], [time, data]]
    """
    logger.debug("Running rebaseTimeSeriesSolar")
    # Removing first and last index because it screws up the interpolation due to the way data gets collected by the irl inverter
    del data[0]
    del data[-1]

    values = []
    times = []
    for index in data:
        values.append(index[1])
        times.append(index[0])
    ts = pd.Series(data=values, index=times)
    # print(ts)
    ts.index = pd.to_datetime(ts.index, utc=True)
    ts = ts.resample("1s").interpolate("time")
    # print(ts)
    rebased = []
    for i, v in ts.items():
        rebased.append([i,v])
    return rebased

def mostIntesiveInterval(data, interval = 900):
    """
    This function calculates the most intensive power interval for a time period

    :param data: List of List: A list with lists containing data points: [[time, data], [time, data]]:  data to be averaged
    :param interval: Int: The duration of the time interval in seconds
    :return: List: [startInterval,TotalPower]
    """
    logger.debug("Running mostIntensiveInterval")
    average = averageOverInterval(data,interval)
    max = average[0]
    for point in average:
        if max[1] > point[1]:
            continue
        max = point
    return max

def averageOverInterval(data, interval = 900):
    """
    This function averages a graph over a given interval: for example: Average value for 00:00-00:15, ...

    :param data: List of List: A list with lists containing data points: [[time, data], [time, data]]:  data to be averaged
    :param interval: Int: Desired interval (in seconds) (standard = 15min)
    :return: List of List: A list with lists containing data points: [[00:00, average], [00:15, Average]]
    """
    logger.debug("Running averageOverInterval")
    values = []
    times = []
    for index in data:
        values.append(index[1])
        times.append(index[0])
    ts = pd.Series(data=values, index=times)
    ts = ts.resample(str(interval)+"s").mean()
    rebased = []
    for i, v in ts.items():
        rebased.append([i,v])
    return rebased

def mergeTimeSeries(time, value):
    """
    This function merges a time list with a value list

    :param time: List: A list with the timestamps
    :param Value: List: A list with the corresponding values
    :return: List of List: A list with lists containing data points: [[time, data], [time, data]]
    """ 
    logger.debug("Running mergeTimeSeries")

    if len(time) != len(value):
        return 0
    result = []
    for i in range(len(value)):
        result.append([time[i], value[i]])
    return result

def periodOverviewList(periodStart, periodEnd, data):
    """
    This function generates the list needed to plot a histogram of popular intervals over a timeperiod

    :param periodStart: DateTime: The start of the period
    :param periodEnd: DateTime: The end of the period
    :return: List of List: A list with lists containing data points: [[time, data], [time, data]]
    """
    logger.debug("Running periodOVerviewList")
    index = pd.date_range(periodStart, periodEnd, freq=str(int(data[0].freq.nanos/10**9))+"s").strftime('%H:%M:%S')
    result = []
    for i in index:
        result.append([i,0])
    
    # Nothing to see here, this is perfectly fine :)
    for i in data:
        for j in result:
            if i.strftime('%H:%M:%S') == j[0]:
                j[1] += 1
                continue
    return result


    
