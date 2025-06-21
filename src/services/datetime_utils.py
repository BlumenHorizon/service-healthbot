from datetime import datetime


def datetime_string_conversion(time: datetime) -> str:
    return time.strftime("%H:%M:%S %d.%m.%Y")
