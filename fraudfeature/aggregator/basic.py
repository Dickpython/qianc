import numpy as np

def Count(vals, missing_value=[None], default=-1):
    """个数"""
    if vals.shape[0] == 0:
        return default 
    result = len([v for v in vals.ravel() if v not in missing_value])
    if result > 0 :
        return result
    else:
        return default


def UniqueCount(vals, missing_value=[None], default=-1):
    """去重个数"""
    if vals.shape[0] == 0:
        return default 
    result = len(set([v for v in vals.ravel() if v not in missing_value]))
    if result > 0:
        return result
    else:
        return default


def Sum(vals, missing_value=[None], default=-1.):
    """累和值"""
    if vals.shape[0] == 0:
        return default 
    result = np.sum([v for v in vals.ravel() if v not in missing_value])
    return result


def Max(vals, missing_value=[None], default=-1.):
    """最大值"""
    if vals.shape[0] > 0:
        x = [v for v in vals.ravel() if v not in missing_value]
        if len(x) > 0:
            return np.max(x)
    return default 


def Min(vals, missing_value=[None], default=-1.):
    """最小值"""
    if vals.shape[0] > 0:
        x = [v for v in vals.ravel() if v not in missing_value]
        if len(x) > 0:
            return np.min(x)
    return default 


def Mean(vals, missing_value=[None], default=-1.):
    """平均值"""
    if vals.shape[0] > 0:
        sum_r = np.sum([v for v in vals.ravel() if v not in missing_value]) 
        return sum_r/vals.shape[0]
    else:
        return default 


def Std(vals, missing_value=[None], default=-1.):
    """标准差"""
    if vals.shape[0] == 0:
        return default
    std_r = np.std([v for v in vals.ravel() if v not in missing_value])
    return std_r 


def Median(vals, missing_value=[None], default=-1.):
    """中位数"""
    if vals.shape[0] == 0:
        return default
    std_r = np.median([v for v in vals.ravel() if v not in missing_value])
    return std_r 


def Quantile25(vals, missing_value=[None], default=-1.):
    """分位数25"""
    if vals.shape[0] == 0:
        return default
    val_seq = np.array([v for v in vals.ravel() if v not in missing_value])
    std_r = np.percentile(val_seq, .25) if val_seq.shape[0] > 0 else default
    return std_r 


def Quantile75(vals, missing_value=[None], default=-1.):
    """分位数75"""
    if vals.shape[0] == 0:
        return default
    val_seq = np.array([v for v in vals.ravel() if v not in missing_value])
    std_r = np.percentile(val_seq, .75) if val_seq.shape[0] > 0 else default
    return std_r 