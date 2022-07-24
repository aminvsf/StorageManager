from config.DateTimeRelated.DateInverter import gregorian_to_jalali


def timestamp_formatter(timestamp) -> str:
    separated_date = [timestamp.year, timestamp.month, timestamp.day]
    jalali_date = '/'.join(list(map(str, gregorian_to_jalali(*separated_date))))
    time = timestamp.astimezone().strftime('%H:%M')
    return f'{time} - {jalali_date}'
