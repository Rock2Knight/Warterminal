from datetime import date as Ddate
from datetime import datetime
from datetime import time as DTime
from typing import Any

def string_from_db_date(db_date: datetime | Ddate | DTime | str | Any, iso_date_format=False) -> str:
    """
    Convert a datetime object to a string
    """
    v = db_date
    if isinstance(db_date, datetime):
        if iso_date_format:
            v = db_date.replace(microsecond=0).astimezone().isoformat()
        else:
            v = db_date.astimezone().strftime("%d.%m.%Y, %H:%M:%S %z")
    elif isinstance(db_date, Ddate):
        if iso_date_format:
            v = db_date.isoformat()
        else:
            v = db_date.strftime("%d.%m.%Y")
    elif isinstance(db_date, DTime):
        v = db_date.replace(microsecond=0).isoformat()
    return v