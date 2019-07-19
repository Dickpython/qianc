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
            if dt.year > 1900 and dt.year < 9999:
                return dt
            else:
                return None
        except ValueError:
            return None


def diff_date(date_tuple, default):
    date_1, date_2 = date_tuple[0], date_tuple[1]
    dt1 = parse_date(date_1)
    dt2 = parse_date(date_2)
    if dt1 and dt2: 
        return (dt1 - dt2).days
    return default


def diff_year(date_tuple, default):
    date_1, date_2 = date_tuple[0], date_tuple[1]
    dt1 = parse_date(date_1)
    dt2 = parse_date(date_2)
    if dt1 and dt2: 
        return dt1.year - dt2.year
    return default


def diff_month(date_tuple, default):
    date_1, date_2 = date_tuple[0], date_tuple[1]
    dt1 = parse_date(date_1)
    dt2 = parse_date(date_2)
    if dt1 and dt2: 
        return (dt1.year - dt2.year)*12 + (dt1.month - dt2.month)
    return default