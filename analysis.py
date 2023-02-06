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
    mostIntensiveIntervalPower = []
    for period in periods:
        time.append(period.periodStart)
        temp = period.statistics()
        totalPower.append(temp["Total power"])
        activeTime.append(temp["Active time"])
        mostIntensiveInterval.append(temp["Most intensive interval"][0])
        mostIntensiveIntervalPower.append(temp["Most intensive interval"][1])

    barPlotTimeSeries(mergeTimeSeries(time,totalPower), "Total power generation per day", 0.5)

    barPlotTimeSeries(mergeTimeSeries(time, activeTime), "Total active hours per day", 0.5)

    barPlotTimeSeries(mergeTimeSeries(time, mostIntensiveIntervalPower), "Most intensive interval average power per day", 0.5)

    barPlotDayOverview(periodOverviewList(periods[0].periodStart, periods[0].periodEnd, mostIntensiveInterval), "Overview of peak average periods")
