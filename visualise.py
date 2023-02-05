import matplotlib.pyplot as plt

def visuTimeseries(data, title = "Graph"):
    time = []
    value = []
    for record in data:
        time.append(record[0])
        value.append(record[1])
    # print(len(value))
    plt.plot(time,value)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Watts (W)")
    plt.show()

def barPlotTimeSeries(data, title = "Graph"):
    """
    This function makes a barplot of the data

    :param data: List of List: A list with lists containing data points: [[time, data], [time, data]]
    :param title: String: the title of the graph
    """
    time = []
    value = []
    for record in data:
        time.append(record[0])
        value.append(record[1])
    
    plt.bar(time, value, width=0.009, align='edge')
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Watts (W)")
    plt.tight_layout()
    plt.grid(axis='x')
    plt.tick_params(axis='both', which='major',
               labelsize=10, labelbottom=True,
               bottom=True, top=True, labeltop=True)
    plt.show()