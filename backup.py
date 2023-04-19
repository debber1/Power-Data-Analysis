from db import *
from datetime import datetime, timedelta 
from config import * 
import pandas as pd
startDay = localToUtc(datetime(2023,2,25,0,0,0))
daysFromStart = datetime.now(timezone.utc)-startDay

config_setup()
print("Difference in days is: " + str(daysFromStart))

data = solarTimePeriod(getValue("host"),getValue("port"),getValue("token"),getValue("org"),getValue("bucket"), startDay , startDay + timedelta(days=daysFromStart.days))
powerData = powerMeterTimePeriod(getValue("host"),getValue("port"),getValue("token"),getValue("org"),getValue("bucket"), startDay  ,startDay + timedelta(days=daysFromStart.days))

print("data has been loaded")

values = []
times = []
for index in data:
    values.append(index[1])
    times.append(index[0])
tsSolar = pd.Series(data=values, index=times)

values = []
times = []
for index in powerData:
    values.append(index[1])
    times.append(index[0])
tsPower = pd.Series(data=values, index=times)

print("data is now a time series")

tsSolar.to_csv('raw_data_solar'+str(datetime.now(timezone.utc))+'.csv', index=True)
tsPower.to_csv('raw_data_power'+str(datetime.now(timezone.utc))+'.csv', index=True)

