import numpy as np


def PassThrough(vals, missing_value=[None], default=np.nan, **kwargs):
    """"""
    if vals.shape[0] == 0:
        return default
    else:
        vals = vals.ravel()
        if vals[0] not in missing_value:
            return vals[0]
        return default


def Count(vals, missing_value=[None], default=np.nan, **kwargs):
    """个数"""
    result = 0
    if vals.shape[0] == 0:
        return default 
    for v in vals.ravel():
         if np.isnan(v) is False and v not in missing_value:
             result += 1
    if result > 0 :
        return result
    else:
        return default


def UniqueCount(vals, missing_value=[None], default=np.nan, **kwargs):
    """去重个数"""
    if vals.shape[0] == 0:
        return default 
    if 'S' or 'U' in vals.dtype:
        result = len(set([v for v in vals.ravel() if v and v not in missing_value]))
    else:
        result = len(set([v for v in vals.ravel() if np.isnan(v) == False and v not in missing_value]))
    if result > 0:
        return result
    else:
        return default


def Sum(vals, missing_value=[None], default=np.nan, **kwargs):
    """累和值"""
    if vals.shape[0] > 0:
        x = [ v for v in vals.ravel() if np.isnan(v) == False and v not in missing_value ]
        if len(x) > 0:
            return np.sum(x)
    return default


def Max(vals, missing_value=[None], default=np.nan, **kwargs):
    """最大值"""
    if vals.shape[0] > 0:
        x = [v for v in vals.ravel() if np.isnan(v) == False and v not in missing_value]
        if len(x) > 0:
            return np.max(x)
    return default 


def Min(vals, missing_value=[None], default=np.nan, **kwargs):
    """最小值"""
    if vals.shape[0] > 0:
        x = [v for v in vals.ravel() if np.isnan(v) == False and v not in missing_value]
        if len(x) > 0:
            return np.min(x)
    return default 


def Mean(vals, missing_value=[None], default=np.nan, **kwargs):
    """平均值"""
    if vals.shape[0] == 0:
        return default
    _t = [v for v in vals.ravel() if np.isnan(v) == False and v not in missing_value]
    if len(_t) > 0:
        return np.mean(_t)
    return default


def Std(vals, missing_value=[None], default=np.nan, **kwargs):
    """标准差"""
    if vals.shape[0] == 0:
        return default
    _t = [v for v in vals.ravel() if np.isnan(v) == False and v not in missing_value]
    if len(_t) > 0:
        return np.std(_t)
    return default


def Median(vals, missing_value=[None], default=np.nan, **kwargs):
    """中位数"""
    if vals.shape[0] == 0:
        return default
    _t = [v for v in vals.ravel() if np.isnan(v) == False and v not in missing_value]
    if len(_t) > 0:
        return np.median(_t)
    return default 


def Quantile25(vals, missing_value=[None], default=np.nan, **kwargs):
    """分位数25"""
    if vals.shape[0] == 0:
        return default
    val_seq = np.array([v for v in vals.ravel() if np.isnan(v) == False and v not in missing_value])
    std_r = np.percentile(val_seq, 25) if val_seq.shape[0] > 0 else default
    return std_r 


def Quantile75(vals, missing_value=[None], default=np.nan, **kwargs):
    """分位数75"""
    if vals.shape[0] == 0:
        return default
    val_seq = np.array([v for v in vals.ravel() if np.isnan(v) == False and v not in missing_value])
    std_r = np.percentile(val_seq, 75) if val_seq.shape[0] > 0 else default
    return std_r 