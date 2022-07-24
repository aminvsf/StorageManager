from datetime import timedelta, datetime

now = datetime.now().astimezone().date()

month_range = now - timedelta(hours=(30 * 24))
week_range = now - timedelta(hours=(7 * 24))
yesterday_range = now - timedelta(hours=24)
