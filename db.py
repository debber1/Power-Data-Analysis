from influxdb_client import InfluxDBClient
from util import *
import logging
logger = logging.getLogger(__name__)

def testConnection(host, port, authToken, myOrg, bucket):
    logger.debug("Testing db connection")
    client = InfluxDBClient(url=host+":"+port, token= authToken, org=myOrg)
    queryApi = client.query_api()
    query = 'from(bucket: "'+bucket+'")\
  |> range(start: -1440m)\
  |> filter(fn: (r) => r["_measurement"] == "W")\
  |> filter(fn: (r) => r["_field"] == "value")\
  |> aggregateWindow(every: 1s, fn: last, createEmpty: false)\
  |> yield(name: "last")'
    result = queryApi.query(org=myOrg, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append([utcToLocal(record.get_time()), record.get_value()])
    return(results)

def solarTimePeriod(host, port, authToken, myOrg, bucket, startDate, stopDate):
    """
    This function takes the relevant data for an influxdb and connects to it. Then, it fetches solar data from startdate to stopDate

    :param host: String: IP of the influxdb
    :param port: String: Port of the influxdb
    :param authToken: String: Token used for identification
    :param myOrg: String: Organisation ID
    :param startDate: DateTime: The date and time where the data starts
    :param endDate: DateTime: The date and time where the data ends
    :return: List of List: A list with lists containing data points: [[time, data], [time, data]]
    """
    logger.debug("Downloading solar time period from server")
    client = InfluxDBClient(url=host+":"+port, token= authToken, org=myOrg)
    queryApi = client.query_api()
    query = 'from(bucket: "'+bucket+'")\
  |> range(start: '+ startDate.strftime('%Y-%m-%dT%H:%M:%SZ')+', stop: '+ stopDate.strftime('%Y-%m-%dT%H:%M:%SZ') +')\
  |> filter(fn: (r) => r["_measurement"] == "W")\
  |> filter(fn: (r) => r["_field"] == "value")\
  |> filter(fn: (r) => r["entity_id"] == "pv_power")\
  |> aggregateWindow(every: 1s, fn: last, createEmpty: false)\
  |> yield(name: "last")'
    result = queryApi.query(org=myOrg, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append([utcToLocal(record.get_time()), record.get_value()])
    return(results)

def powerMeterTimePeriod(host, port, authToken, myOrg, bucket, startDate, stopDate):
    """
    This function takes the relevant data for an influxdb and connects to it. Then, it fetches powerMeter data from startdate to stopDate

    :param host: String: IP of the influxdb
    :param port: String: Port of the influxdb
    :param authToken: String: Token used for identification
    :param myOrg: String: Organisation ID
    :param startDate: DateTime: The date and time where the data starts
    :param endDate: DateTime: The date and time where the data ends
    :return: List of List: A list with lists containing data points: [[time, data], [time, data]]
    """
    logger.debug("Downloading power time period from server")
    client = InfluxDBClient(url=host+":"+port, token= authToken, org=myOrg)
    queryApi = client.query_api()
    query = 'from(bucket: "'+bucket+'")\
  |> range(start: '+ startDate.strftime('%Y-%m-%dT%H:%M:%SZ')+', stop: '+ stopDate.strftime('%Y-%m-%dT%H:%M:%SZ') +')\
  |> filter(fn: (r) => r["_measurement"] == "W")\
  |> filter(fn: (r) => r["_field"] == "value")\
  |> filter(fn: (r) => r["entity_id"] == "p1_meter_5c2faf05011e_active_power")\
  |> aggregateWindow(every: 1s, fn: last, createEmpty: false)\
  |> yield(name: "last")'
    result = queryApi.query(org=myOrg, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append([utcToLocal(record.get_time()), record.get_value()])
    return(results)
