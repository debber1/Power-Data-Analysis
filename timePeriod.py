from visualise import *
from util import *
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
        self.periodName = periodName
        self.periodStart = periodStart
        self.periodEnd = periodEnd
        self.solarData = solarData
        self.powerData = powerData
    
    def visualiseSolar(self):
        """
        This function visualises the solar data of a timeperiod
        """
        visuTimeseries(self.solarData, "Solar graph for "+self.periodName)
        barPlotTimeSeries(averageOverInterval(self.solarData), "15 minute solar averages for "+self.periodName)

    def visualise(self):
        """
        This function visualises the data of a timeperiod
        """

        visuThreeTimeseries(self.powerData, self.solarData, "Graph for "+self.periodName)
    
    def statistics(self):
        """
        This function calculates key statistics based on the data

        :return: Dict: A dictionary with the results of the statistical analysis
        """
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