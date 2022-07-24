from pytz import timezone


def date_time_validator(datetime):
    now = datetime.now(timezone('Iran'))
    return datetime > now
