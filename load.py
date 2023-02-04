from util import *
from db import *
from datetime import datetime, timedelta 
from timePeriod import *
def loadDataDayScale(startDay, numberOfDays):
    """
    This function loads the relevant data for a timeperiod and devides it in daily segments

    :param startDay: DateTime: the day where datacollection should start
    :param numberOfDays: Int: The number of days we want to pull the data from
    :return: List of timePeriod: List of class with relevant data for a segment of a day
    """
    days = []
    for day in range(0,numberOfDays):
        print("loading day "+str(day + 1)+" of "+str(numberOfDays))
        data = solarTimePeriod(getValue("host"),getValue("port"),getValue("token"),getValue("org"),getValue("bucket"), startDay + timedelta(days=day), startDay + timedelta(days=day+1))
        period = timePeriodData((startDay+timedelta(days=day)).strftime("%d/%m/%Y"), startDay + timedelta(days=day), startDay + timedelta(days=day+1), data)
        days.append(period)
    return days
 