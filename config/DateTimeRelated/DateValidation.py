from datetime import datetime


def date_validation(start_date, end_date, date):
    fmt = '%Y-%m-%d'
    date = datetime.strptime(date, fmt)
    end_date = datetime.strptime(end_date, fmt)
    start_date = datetime.strptime(start_date, fmt)
    if (start_date - date).days <= 0 <= (end_date - date).days:
        return True
    return False


def date_expiration_validation(date, expire_date):
    fmt = '%Y-%m-%d'
    date = datetime.strptime(date, fmt)
    expire_date = datetime.strptime(expire_date, fmt)
    if (expire_date - date).days >= 0:
        return True
    return False
