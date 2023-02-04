from visualise import *
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
