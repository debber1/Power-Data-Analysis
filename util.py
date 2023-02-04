from datetime import datetime, timezone, timedelta
from config import *
import timePeriod

def utcToLocal(date):
    return date.replace(tzinfo=timezone.utc).astimezone(tz=None)
