import numpy as np
import re


def equal(param, vals):
    _func = np.vectorize(lambda x: True if x == param else False)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out

def not_equal(param, vals):
    _func = np.vectorize(lambda x: True if x != param else False)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out

def match(param, vals):
    _func = np.vectorize(lambda x: True if param in x else False)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out

def not_match(param, vals):
    _func = np.vectorize(lambda x: True if param not in x else False)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out

def regex_match(param, vals):
    m_regex = re.compile(param)
    _func = np.vectorize(lambda x: True if m_regex.search(x) is not None else False)
    out = _func(vals) if vals.shape[0] != 0 else vals.reshape(-1, 1)
    return out

def parse_all(param, vals):
    return np.array([True] * vals.shape[0])