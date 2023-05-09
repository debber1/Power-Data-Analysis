from visualise import *
from util import *
import logging
logger = logging.getLogger(__name__)
class timePeriodData:

    #Constructor
    def __init__(self, periodName, periodStart, periodEnd, solarData, powerData):
        """
        This is the constructor of a time period.

        :param periodName: String: name of the period
        :param periodStart: DateTime: Start of the period
        :param periodEnd: DateTime: End of the period
        :param solarData: List of List: A List containing lists of datapoints, [[time, data], [time, data]]
        :param powerData: List of List: A List containing lists of datapoints, [[time, data], [time, data]]
        """
        logger.debug("Making a new instance of timePeriodData")
        self.periodName = periodName
        self.periodStart = periodStart
        self.periodEnd = periodEnd
        self.solarData = solarData
        self.powerData = powerData
    
    def visualiseSolar(self):
        """
        This function visualises the solar data of a timeperiod
        """
        logger.debug("Running solar visualisation")
        visuTimeseries(self.solarData, "Solar graph for "+self.periodName)
        barPlotTimeSeries(averageOverInterval(self.solarData), "15 minute solar averages for "+self.periodName)

    def visualisePower(self):
        """
        This function visualises the power data of a timeperiod
        """
        logger.debug("Running power visualisation")
        visuTimeseries(self.powerData, "Power graph for "+self.periodName)
        barPlotTimeSeries(averageOverInterval(self.powerData), "15 minute power averages for "+self.periodName)

    def visualise(self):
        """
        This function visualises the data of a timeperiod
        """

        logger.debug("Running visualisation")
        visuThreeTimeseries(self.powerData, self.solarData, "Graph for "+self.periodName)
    
    def statistics(self):
        """
        This function calculates key statistics based on the data

        :return: Dict: A dictionary with the results of the statistical analysis
        """
        logger.debug("Running statistics")
        results = {}
        # Calculate the total watt hours produced by the solar panels
        results["Total power"] = integralTimeSeries(self.solarData)

        # Calculate the total amount of active hours for the solar panels
        results["Active time"] = activeTime(self.solarData)

        # Calculate the most intensive period of solar generation
        results["Most intensive interval"] = mostIntesiveInterval(self.solarData)

        # Calculate the most intensive period of power usage
        results["Most intensive interval power"] = mostIntesiveInterval(self.powerData)
        return results

    def printStats(self):
        """
        This function prints the results of the statistical analysis
        """
        stats = self.statistics()
        print("Statistics for: "+self.periodName)
        print(stats)    