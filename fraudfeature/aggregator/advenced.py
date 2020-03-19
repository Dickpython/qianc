import numpy as np
from collections import Counter

def DummyCount(vals, param, missing_value=[None], default=-1.):
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


def MulMax(vals, param, missing_value=[None], default=np.nan):
    """最大值"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.amax(vals,axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulMax'] = _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulMax'] = np.max(x) if len(x) > 0 else default
    # print("result", result)
    return result


def MulSum(vals, param, missing_value=[None], default=np.nan):
    """累计值"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.sum(vals, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulSum'] = _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulSum'] = np.sum(x) if len(x) > 0 else default
    # print(result)
    return result


def MulMin(vals, param, missing_value=[None], default=np.nan):
    """最小值"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.amin(vals, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulMin'] = _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulMin'] = np.min(x) if len(x) > 0 else default
    # print(result)
    return result


def MulMean(vals, param, missing_value=[None], default=np.nan):
    """平均值"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.mean(vals, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulMean'] = _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulMean'] = np.mean(x) if len(x) > 0 else default
    # print(result)
    return result


def MulStd(vals, param, missing_value=[None], default=np.nan):
    """标准差"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.std(vals, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulStd'] = _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulStd'] = np.std(x) if len(x) > 0 else default
    # print(result)
    return result


def MulQuantile25(vals, param, missing_value=[None], default=np.nan):
    """分位数25"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.percentile(vals, 25,axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulQuantile25'] = _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulQuantile25'] = np.percentile(x, 25) if len(x) > 0 else default
    # print(result)
    return result


def MulQuantile75(vals, param, missing_value=[None], default=np.nan):
    """分位数75"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.percentile(vals, 75, axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulQuantile75'] = _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulQuantile75'] = np.percentile(x, 75) if len(x) > 0 else default
    # print(result)
    return result


def MulMedian(vals, param, missing_value=[None], default=np.nan):
    """分位数75"""
    _M = [k for k in param.keys()]
    _M.sort()
    result = {}
    if vals.shape[0] > 0:
        _vals = np.median(vals,axis=0)
        for i,m in enumerate(_M):
            result[param.get(m)+'_MulMedian'] = _vals[i]
        # for i, m in enumerate(_M):
        #     _vals = np.take(vals, i, axis=1)
        #     x = [v for v in _vals if np.isnan(v) == False and v not in missing_value]
        #     result[param.get(m) + '_MulMedian'] = np.median(x) if len(x) > 0 else default
    # print(result)
    return result