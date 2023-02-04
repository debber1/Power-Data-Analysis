from datetime import datetime, timezone, timedelta
from config import *

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

def onTime(data):
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