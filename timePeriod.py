from visualise import *
from util import *
class timePeriodData:

    #Constructor
    def __init__(self, periodName, periodStart, periodEnd, solarData):
        """
        This is the constructor of a time period.

        :param periodName: String: name of the period
        :param periodStart: DateTime: Start of the period
        :param periodEnd: DateTime: End of the period
        :param solarData: List of List: A List containing lists of datapoints, [[time, data], [time, data]]
        """
        self.periodName = periodName
        self.periodStart = periodStart
        self.periodEnd = periodEnd
        self.solarData = solarData
    
    def visualise(self):
        """
        This function visualises the data of a timeperiod
        """
        visuTimeseries(self.solarData, "Graph for "+self.periodName)
    
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

        return results

    def printStats(self):
        """
        This function prints the results of the statistical analysis
        """
        stats = self.statistics()
        print("Statistics for: "+self.periodName)
        print(stats)    