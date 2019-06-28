import numpy as np


def sum(vals, missing_value=[None], default=-1):
    """累和值"""
    if vals.shape[0] == 0:
        return default 
    result = np.sum([v for v in vals.ravel() if v not in missing_value])
    return result


def avg(vals, missing_value=[None], default=-1):
    """平均值"""
    if vals.shape[0] > 0:
        sum_r = np.sum([v for v in vals.ravel() if v not in missing_value]) 
        return sum_r/vals.shape[0]
    else:
        return default 


def std(vals, missing_value=[None], default=-1):
    """平均值"""
    if vals.shape[0] == 0:
        return default
    std_r = np.std([v for v in vals.ravel() if v not in missing_value])
    return std_r   