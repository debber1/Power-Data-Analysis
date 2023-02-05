from timePeriod import *
from util import *
from visualise import *
import datetime
def solarAnalysis(periods):
    """
    This function performs an analysis over multiple timeperiods

    :param periods: List of timePeriodData: a list of time period data
    """

    # Extracting key statistics
    time = []
    totalPower = []
    activeTime = []
    mostIntensiveInterval = []
    for period in periods:
        time.append(period.periodStart)
        temp = period.statistics()
        totalPower.append(temp["Total power"])
        activeTime.append(temp["Active time"])
        mostIntensiveInterval.append(temp["Most intensive interval"])

    dataTotalPower = []
    for i in range(len(totalPower)):
        dataTotalPower.append([time[i],totalPower[i]])
    barPlotTimeSeries(dataTotalPower, "Total power generation per day", 0.5)

    dataActiveTime = []
    for i in range(len(activeTime)):
        dataActiveTime.append([time[i],activeTime[i]])
    barPlotTimeSeries(dataActiveTime, "Total active hours per day", 0.5)

    index = pd.date_range(periods[0].periodStart, periods[0].periodEnd, freq=str(int(mostIntensiveInterval[0][0].freq.nanos/10**9))+"s").strftime('%H:%M:%S')
    averagePeriodList = []
    for i in index:
        averagePeriodList.append([i,0])
    
    for i in mostIntensiveInterval:
        for j in averagePeriodList:
            if i[0].strftime('%H:%M:%S') == j[0]:
                j[1] += 1
                continue
    barPlotDayOverview(averagePeriodList, "Overview of peak average periods")