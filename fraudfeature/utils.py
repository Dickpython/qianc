from datetime import datetime
from dateutil.parser import parse


def parse_date(date_str, dayfirst=False):
    date_str = date_str.split('.')[0] if len(date_str)>20 else date_str.replace('.','-')
    # to-do: dt.year need to be updated！
    try:
        dt = parse(date_str, fuzzy=True, dayfirst=dayfirst)
        return dt
    except ValueError:
        try:
            dt = datetime.fromtimestamp(int(date_str))
            if dt.year > 1900 and dt.year < 2050:
                return dt
            else:
                return None
        except ValueError:
            return None
