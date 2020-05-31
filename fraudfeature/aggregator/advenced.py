import numpy as np
from collections import Counter

def DummyCount(vals, param, default, missing_value=[]):
    """个数"""
    if vals.shape[0] == 0:
        return {t+'_DummyCount': default for t in param.values()}
    c = Counter([v for v in vals.ravel() if v not in missing_value])
    result = {}
    _M = [k for k in param.keys()]
    _M.sort()
    visited = set()
    for origin in _M:
        _v = c.get(origin, 0)
        target = param[origin]
        if target in visited :
            result[target+"_DummyCount"] = result[target+"_DummyCount"] + _v
        elif target not in visited :
            result[target+"_DummyCount"] = _v if _v > 0 else default
            visited.add(target)
    return result


def MulMax(vals, param, default, missing_value=[]):
    """最大值"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.nanmax(vals,axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulMax'] = default if np.isnan(_vals[i]) else _vals[i]
    return result


def MulSum(vals, param, default, missing_value=[]):
    """累计值"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.nansum(vals, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulSum'] = default if np.isnan(_vals[i]) else _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulSum'] = np.sum(x) if len(x) > 0 else default
    return result


def MulMin(vals, param, default, missing_value=[]):
    """最小值"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.nanmin(vals, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulMin'] = default if np.isnan(_vals[i]) else _vals[i]
    return result


def MulMean(vals, param, default,missing_value=[]):
    """平均值"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.nanmean(vals, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulMean'] = default if np.isnan(_vals[i]) else _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulMean'] = np.mean(x) if len(x) > 0 else default
    return result


def MulStd(vals, param, default, missing_value=[]):
    """标准差"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.nanstd(vals, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulStd'] = default if np.isnan(_vals[i]) else _vals[i]
    return result


def MulQuantile25(vals, param, default, missing_value=[]):
    """分位数25"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.nanpercentile(vals, 25,axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulQuantile25'] = default if np.isnan(_vals[i]) else _vals[i]
    return result


def MulQuantile75(vals, param, default, missing_value=[]):
    """分位数75"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.nanpercentile(vals, 75, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulQuantile75'] = default if np.isnan(_vals[i]) else _vals[i]
    return result


def MulMedian(vals, param, default, missing_value=[]):
    """分位数75"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.nanmedian(vals,axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulMedian'] = default if np.isnan(_vals[i]) else _vals[i]
    return result


def MulQuantile(vals, param, default, missing_value=[]):
    """分位数"""
    _M = [k for k in param.keys()]
    _M.sort()
    hd = [param.get(v) for v in _M]
    if len(set(hd)) != len(param):
        print("[ERROR] MulQuantile param exist dupe values!")
        raise Exception
    result = {}
    if vals.shape[0] > 0:
        _vals = np.nanpercentile(vals, [25, 50, 75], axis=0)
        for i,_v in enumerate(_vals):
            result.update({k+'_MulQuantile'+str((i+1)*25):default if np.isnan(v) else v for k, v in zip(hd,_v)})
    return result