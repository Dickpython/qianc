import numpy as np
from .utils import parse_date, diff_date, diff_month, diff_year


def parse_normal_time(vals, missing_value=[None], default=-1):
    _func = np.vectorize(parse_date)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out

def parse_float(vals, missing_value=[None], default=-1):
    _func = np.vectorize(lambda x: float(x) if x != "" and x is not None else default, otypes=[float])
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def parse_str(vals, missing_value=[None], default=-1):
    _func = np.vectorize(lambda x: str(x) if x != "" and x is not None else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def day_interval(vals, missing_value=[None], default=-1):
    return np.array([diff_date(v, default)  for v in vals])


def month_interval(vals, missing_value=[None], default=-1):
    return np.array([diff_month(v, default)  for v in vals])


def year_interval(vals, missing_value=[None], default=-1):
    return np.array([diff_year(v, default)  for v in vals])


def parse_ratio:
    pass
