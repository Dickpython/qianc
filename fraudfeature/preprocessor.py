import numpy as np
from datetime import datetime
from .util import parse_date, diff_date, diff_month, diff_year
from .util import similarity
from .util import find_region, find_city, find_citytier


def parse_normal_time(vals, missing_value=[None], default=datetime(1900,1,1), **kwargs):
    _func = np.vectorize(lambda x: parse_date(x) if parse_date(x) else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def parse_float(vals, missing_value=[None], default=np.nan, **kwargs):
    _func = np.vectorize(lambda x: float(x) if x != "" and x is not None and x not in missing_value else default, otypes=[float])
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def parse_str(vals, missing_value=[None], default=np.nan, **kwargs):
    _func = np.vectorize(lambda x: str(x) if x != "" and x is not None and x not in missing_value else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def day_interval(vals, missing_value=[None], default=np.nan, **kwargs):
    return np.array([diff_date(v, default) for v in vals])


def month_interval(vals, missing_value=[None], default=np.nan, **kwargs):
    return np.array([diff_month(v, default)  for v in vals])


def year_interval(vals, missing_value=[None], default=np.nan, **kwargs):
    return np.array([diff_year(v, default)  for v in vals])


def parse_ratio(vals, missing_value=[None], default=np.nan, **kwargs):
    result = np.array([float(v[0])/float(v[1]) if v[0] not in missing_value \
        and v[1] not in missing_value and float(v[1]) >0 else default for v in vals])
    # print(result)
    return result


def cal_similarity(vals, missing_value=[None], default=np.nan, **kwargs):
    _t = []
    for v in vals:
        if v[0] in missing_value or v[1] in missing_value:
            _t.append(default)
        else:
            _t.append(similarity(v, default))
    return np.array(_t)


def parse_region(vals, missing_value=[None], default=np.nan, **kwargs):
    _func = np.vectorize(lambda x: find_region(x) if x != "" and x is not None else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def parse_city(vals, missing_value=[None], default=np.nan, **kwargs):
    _func = np.vectorize(lambda x: find_city(x) if x != "" and x is not None else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def parse_citytier(vals, missing_value=[None], default=np.nan, **kwargs):
    _func = np.vectorize(lambda x: find_citytier(x) if x != "" and x is not None else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def parse_24month(vals, param, missing_value=[None], default=np.nan, **kwargs):
    _M = [k for k in param.keys()]
    _M.sort()
    def _LPS(x):
        if x != "" and x is not None:
            return [x.count(v) for v in _M]
        else:
            return [0]*len(param)
    if vals.shape[0] != 0 :
        return np.array([_LPS(v) for v in vals.ravel()]) 
    else:
        return np.array([[0]*len(param)])


def parse_merge(vals, missing_value=[None], **kwargs):
    out = []
    for v in vals:
        out.append(sum([int(_v) for _v in v if _v not in missing_value]))
    return np.array(out)
