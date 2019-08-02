import numpy as np
from collections import Counter

def DummyCount(vals, param, missing_value=[None], default=-1.):
    """个数"""
    if vals.shape[0] == 0:
        return {t+'_DummyCount': default for t in param.values()}
    c = Counter([v for v in vals.ravel() if v not in missing_value])
    result={}
    for origin, target in param.items():
        _v = c.get(origin, 0)
        result[target+"_DummyCount"] = _v if _v > 0 else default
    return result