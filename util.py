from datetime import datetime, timezone, timedelta
from config import *
import pandas as pd

def utcToLocal(date):
    return date.replace(tzinfo=timezone.utc).astimezone(tz=None)

def integralTimeSeries(data):
    """
    This function calculates the discrete integral of a timeseries while taking real life limitations into account (such as reporting at the beginning and ending of a solar cycle)

    :param data: List of List: A list with lists containing data points: [[time, data], [time, data]]
    :return: Int: total power used/produced over the timeperiod
    """
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
    ts = ts.resample("1s").interpolate("time")
    # print(ts)
    rebased = []
    for i, v in ts.items():
        rebased.append([i,v])
    return rebased