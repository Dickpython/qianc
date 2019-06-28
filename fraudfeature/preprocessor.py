import numpy as np
from .utils import parse_date


def parse_normal_time(vals, missing_value=[None], default=-1):
    _func = np.vectorize(parse_date)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out


def parse_float(vals, missing_value=[None], default=-1):
    _func = np.vectorize(lambda x: float(x) if x != "" and x is not None else default)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out
