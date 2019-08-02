import numpy as np
from datetime import datetime
from .util.common import parse_date, diff_date, diff_month, diff_year
from .util.common import similarity
from .util.common import find_region, find_city, find_citytier


def parse_normal_time(vals, missing_value=[None], default=datetime(1900,1,1)):
    _func = np.vectorize(lambda x: parse_date(x) if parse_date(x) else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def parse_float(vals, missing_value=[None], default=np.nan):
    _func = np.vectorize(lambda x: float(x) if x != "" and x is not None else default, otypes=[float])
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def parse_str(vals, missing_value=[None], default=np.nan):
    _func = np.vectorize(lambda x: str(x) if x != "" and x is not None else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def day_interval(vals, missing_value=[None], default=np.nan):
    return np.array([diff_date(v, default) for v in vals])


def month_interval(vals, missing_value=[None], default=np.nan):
    return np.array([diff_month(v, default)  for v in vals])


def year_interval(vals, missing_value=[None], default=np.nan):
    return np.array([diff_year(v, default)  for v in vals])


def parse_ratio(vals, missing_value=[None], default=np.nan):
    return 


def cal_similarity(vals, missing_value=[None], default=np.nan):
    _t = []
    for v in vals:
        if v[0] in missing_value or v[1] in missing_value:
            _t.append(default)
        else:
            _t.append(similarity(v, default))
    return np.array(_t)


def parse_region(vals, missing_value=[None], default=np.nan):
    _func = np.vectorize(lambda x: find_region(x) if x != "" and x is not None else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out
