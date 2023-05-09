import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import time
import logging
logger = logging.getLogger(__name__)
def visuTimeseries(data, title = "Graph", save = False, savePath = "./"):
    plt.ioff()
    time1 = []
    value = []
    for record in data:
        time1.append(record[0])
        value.append(record[1])
    # print(len(value))
    plt.plot(time1,value)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Watts (W)")
    if(not save):
        plt.show()
    else:
        plt.savefig(savePath + title)
        plt.close()

def visuThreeTimeseries(data1, data2, title = "Graph", save = False, savePath = "./"):
    plt.ioff()
    time1 = []
    time2 = []
    time3 = []
    value1 = []
    value2 = []
    value3 = []
    for record in data1:
        time1.append(record[0])
        value1.append(record[1])
    for record in data2:
        time2.append(record[0])
        value2.append(record[1])
    ts1 = pd.Series(data=value1, index=time1)
    ts2 = pd.Series(data=value2, index=time2)
    ts3 = ts1+ts2
    # print(len(value))
    plt.plot(ts1)
    plt.plot(ts2)
    plt.plot(ts3)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Watts (W)")
    if(not save):
        plt.show()
    else:
        plt.savefig(savePath + title)
        plt.close()

def barPlotTimeSeries(data, title = "Graph", barWidth = 0.009, save = False, savePath = "./"):
    """
    This function makes a barplot of the data

    :param data: List of List: A list with lists containing data points: [[time, data], [time, data]]
    :param title: String: the title of the graph
    """
    plt.ioff()
    time1 = []
    value = []
    for record in data:
        time1.append(record[0])
        value.append(record[1])
    
    plt.bar(time1, value, width=barWidth, align='edge')
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Watts (W)")
    plt.tight_layout()
    plt.grid(axis='x')
    plt.tick_params(axis='both', which='major',
               labelsize=10, labelbottom=True,
               bottom=True, top=True, labeltop=True)
    if(not save):
        plt.show()
    else:
        plt.savefig(savePath + title)
        plt.close()

def barPlotDayOverview(data, title = "Graph", barWidth = 0.9, save = False, savePath = "./"):
    """
    This function makes a barplot of the data

    :param data: List of List: A list with lists containing data points: [[time, data], [time, data]]
    :param title: String: the title of the graph
    """
    plt.ioff()
    time1 = []
    value = []
    for record in data:
        time1.append(record[0])
        value.append(record[1])

    plt.bar(time1, value, width=barWidth, align='edge')
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.xticks(rotation=90)
    plt.autoscale()
    if(not save):
        plt.show()
    else:
        plt.savefig(savePath + title)
        plt.close()