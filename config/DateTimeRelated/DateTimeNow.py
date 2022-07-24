from datetime import datetime

from pytz import timezone


def date_time_now():
    return datetime.now(timezone('Iran'))
