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