import numpy as np
from datetime import datetime, timedelta
from .preprocessor import parse_normal_time
#from numba import jit


CHAR_PRE_FUNC = ('parse_str', 'parse_region', 'parse_city', 'parse_citytier')
NUMR_PRE_FUNC = ('parse_float', 'day_interval', 'month_interval', 'year_interval',
    'parse_ratio', 'cal_similarity')
TIME_PRE_FUNC = ('parse_normal_time')

#@jit(nopython=True)
def _apply_timewindow(conf, col_index, tw, arr):
    aply_idx = int(col_index[conf.get("time_index").get("apply_dt")])
    evnt_idx = int(col_index[conf.get("time_index").get("event_dt")])
    _ta = parse_normal_time(np.take(arr, aply_idx, axis=1))
    _te = parse_normal_time(np.take(arr, evnt_idx, axis=1))
    return (_ta - _te) <= timedelta(tw)     


#@jit(nopython=True)
def _check_time_index_validity(conf, col_index, arr):
    # to-do: add parse time function 
    if "time_index" not in conf:
        return arr
    aply_idx = int(col_index[conf.get("time_index").get("apply_dt")])
    evnt_idx = int(col_index[conf.get("time_index").get("event_dt")])
    _ta = np.take(arr, aply_idx, axis=1)
    _te = np.take(arr, evnt_idx, axis=1)
    valid_tm = (_ta >= _te).ravel()
    return np.compress(valid_tm, arr, axis=0)


class Conf:
    def __init__(self, path, conf, sep='\t', domain=None, cn_domain=None,
        default=-99999., default_str="NotAvailable", default_time=datetime(1900,1,1), missing_value=[None]):
        self.conf = conf
        self.domain = domain
        self.cn_domain=cn_domain
        self.output_header = None
        self.output_cn_header = None
        self.key_index = []
        self.selected_feature_index = []
        self.time_index_id = []
        self.col_index = {}
        self.index_col = {}
        self.sep = sep
        self.default = default
        self.default_str = default_str
        self.missing_value = missing_value
        self.default_time = default_time
        self.valid = self.check_conf()
        if self.valid:
            self._load_index(path)
            self.export_feature_dict()
        else:
            pass
            # logger.Error invalid! 
 
    def check_conf(self):
        if "index" in self.conf and len(self.conf.get("index"))>0 and \
            "feature_entries" in self.conf and len(self.conf.get("feature_entries")) > 0:
            return True
        else:
            # log.Error missing index in config
            return False

    def _load_index(self, path):
        header = None
        with open(path, "rb") as read_file:
            header = read_file.readline().decode().strip('\n').split(self.sep)
        self.col_index = {h:i for i,h in enumerate(header)}
        self.index_col = {i:h for i,h in enumerate(header)}
        self.primary_key = self.conf.get("index")
        self.key_index = [self.col_index[k] for k in self.conf.get("index")]

    def export_feature_dict(self):
        time_window = self.conf.get("time_window") if "time_window" in self.conf else [None]
        filter = self.conf.get("filters") if "filters" in self.conf else [None]
        name, cn_name = [], []
        for tw in time_window:
            _tw, _cn_tw = "", ""
            _tw = "" if tw is None else _tw + "".join(["Last", str(tw), "Days"])
            _cn_tw = "" if tw is None else _cn_tw + "".join(["过去", str(tw), "天"])

            for f in filter:
                fn    = f.get("name") if f is not None else ""
                fn_cn = f.get("cn_name") if f is not None else ""
                # add time window in name
                fn    = "__".join([ fn, _tw]) if _tw != "" else fn
                fn_cn = "__".join([ fn_cn, _cn_tw ]) if _cn_tw != "" else fn_cn

                for fe_entry in self.conf.get("feature_entries"):
                    _pnm    = "__".join([ fn, fe_entry.get("prefix")]) if fn != '' else fe_entry.get("prefix")
                    _pnm_cn = "__".join([ fn_cn, fe_entry.get("desc")]) if fn_cn != '' else fe_entry.get("desc")
                    for f in fe_entry.get("aggregator"):
                        if fe_entry.get("param") and isinstance(fe_entry.get("param"), dict):
                            _M = [k for k in fe_entry.get("param").keys()]
                            _M.sort()
                            visited = set()
                            if f.__name__ in ('MulQuantile'):
                                for r in ['25','50','75']:
                                    for target in _M:
                                        tsf_val = fe_entry.get("param").get(target)
                                        if tsf_val in visited:
                                            continue
                                        else:
                                            visited.add(tsf_val)
                                            name.append("_".join([_pnm, tsf_val, f.__name__+r]))
                                            cn_name.append("_".join([_pnm_cn, tsf_val, f.__doc__+r]))
                            else:
                                for target in _M:
                                    tsf_val = fe_entry.get("param").get(target)
                                    if tsf_val in visited:
                                        continue
                                    else:
                                        visited.add(tsf_val)
                                        name.append("_".join([_pnm, tsf_val, f.__name__]))
                                        cn_name.append("_".join([_pnm_cn, tsf_val, f.__doc__]))
                        else:
                            if f.__name__ != 'PassThrough':
                                name.append("_".join([_pnm, f.__name__]))
                                cn_name.append("_".join([_pnm_cn, f.__doc__]))
                            else:
                                name.append(_pnm)
                                cn_name.append(_pnm_cn)
                        
        self.output_header = self.primary_key + [self.domain + n if self.domain else n for n in name] 
        self.output_cn_header = self.primary_key + [self.cn_domain + n if self.cn_domain else n for n in cn_name]

    def apply_key(self, vals):
        val = vals.decode().strip("\n").split(self.sep)
        return [val[i] for i in self.key_index]

    def pipefunc(self, params_tuple):
        seq_no, vals = params_tuple
        # skip the first empty sequence
        if vals == []:
            return seq_no, None
        arr = np.array([np.array(v.decode().strip("\n").split(self.sep)) for v in vals], order='F') 
        # If use `time_index`, check if `vals` is valid, if not return empty `clean`.
        if "time_index" not in self.conf:
            arr = _check_time_index_validity(self.conf, self.col_index, arr)       
        return self._compute(seq_no, arr)

    def apply_agg(self, func, arr, pre, param=None):
        result, name = [], []
        if isinstance(func, list):
            for f in func:
                if f.__name__ == 'PassThrough':
                    _default = self.default if pre and pre.__name__ in NUMR_PRE_FUNC else self.default_str
                _r = f(vals=arr, missing_value=self.missing_value, default=_default, param=param)
                if isinstance(_r, dict):
                    # Dictionaries are insertion ordered. 
                    # As of Python 3.6, for the CPython implementation of Python
                    # dictionaries remember the order of items inserted. 
                    for _n, _v in _r.items():
                        result.append(_v)
                        name.append(_n)
                else:
                    result.append(_r)
                    name.append(f.__name__)
        return name, result

    def apply_preprr(self, func, arr, param):
        _default = self.default
        if func.__name__ in CHAR_PRE_FUNC : _default = self.default_str
        if func.__name__ in TIME_PRE_FUNC : _default = self.default_time
        f_arr = func(arr, missing_value=self.missing_value, param=param, default=_default)
        return f_arr

    def apply_filter(self, func, param, arr):
        if isinstance(func, list) and isinstance(param, list):
            filter_cond = np.array([True] * arr.shape[0])
            for i, cmps in enumerate(zip(func, param)):
                f, p = cmps
                filter_cond = filter_cond & f(param=p, vals=arr[:,i]) 
            return filter_cond
        else:
            # log.Error `func` and `param` need to be lists.
            return

    def _compute(self, seq_no, vals):
        result = [v for v in np.take(vals, self.key_index, axis=1)[0]]
        # Use `time_window` then combine with `filters` as criteria to select array data.
        time_window = self.conf.get("time_window") if "time_window" in self.conf else [None]
        for tw in time_window:
            tm_cond = _apply_timewindow(self.conf, self.col_index, tw, vals) if tw else np.array([True] * vals.shape[0])
            combine_cond = tm_cond
            for f in self.conf.get("filters", [None]):
                if f is not None:
                    filter_idx = [ self.col_index[f] for f in f.get("feature") ]
                    slim_filter_arr = np.take(vals, filter_idx, axis=1)
                    filter_cond = self.apply_filter(func=f.get("func"), param=f.get("value"), arr=slim_filter_arr)
                    combine_cond = tm_cond & filter_cond    
                arr_ready = np.compress(combine_cond, vals, axis=0)

                for fe_entry in self.conf.get("feature_entries"):
                    _preprc_func = fe_entry.get("preprocessor")
                    f_idx = [self.col_index[f] for f in fe_entry.get("feature")]
                    f_arr = np.take(arr_ready, f_idx, axis=1)
                    if _preprc_func:
                        f_arr = self.apply_preprr(func=_preprc_func, arr=f_arr, param=fe_entry.get("param"))
                    _fn, _rslt = self.apply_agg(func=fe_entry.get("aggregator"), arr=f_arr, pre=_preprc_func, param=fe_entry.get("param"))
                    for d in _rslt:
                        result.append(d)
        return seq_no, result