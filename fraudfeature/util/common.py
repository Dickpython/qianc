from datetime import datetime
from dateutil.parser import parse
from fuzzywuzzy.fuzz import ratio
from .place import __byname


def parse_date(date_str, dayfirst=False):
    if date_str in ('00000000','00000101','19000101','1900.01','1900.01.01','1900','190001'):
        return None
    if len(date_str) == 4:
        date_str = date_str + '-01-01'
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


def similarity(str_tuple, default):
    str_1, str_2 = str_tuple[0], str_tuple[1]
    if str_1 and str_2:
        return ratio(str_1, str_2)
    return default


def find_region(x):
    d = __byname(x)
    if d:
        return d.region()
    return None


def find_city(x):
    d = __byname(x)
    if d:
        c = d.curcity()
        if c:
            return d.curcity().city
    return None


def find_citytier(x):
    d = __byname(x)
    if d:
        return d.tier()
    return None
