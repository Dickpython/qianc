import numpy as np
from datetime import datetime, timedelta
from .preprocessor import parse_normal_time
from numba import jit


def apply_agg(func, arr):
    result, name = [], []
    if isinstance(func, list):
        for f in func:
            result.append(f(arr))
            name.append(f.__name__)
    return name, result


def apply_filter(func, param, arr):
    if isinstance(func, list) and isinstance(param, list):
        filter_cond = np.array([True] * arr.shape[0])
        for i, cmps in enumerate(zip(func, param)):
            f, p = cmps
            filter_cond = filter_cond & f(param=p, vals=arr[:,i]) 
        return filter_cond
    else:
        # log.Error `func` and `param` need to be lists.
        return

@jit(nopython=True)
def _apply_timewindow(conf, col_index, tw, arr):
    aply_idx = int(col_index[conf.get("time_index").get("apply_dt")])
    evnt_idx = int(col_index[conf.get("time_index").get("event_dt")])
    _ta = parse_normal_time(np.take(arr, aply_idx, axis=1))
    _te = parse_normal_time(np.take(arr, evnt_idx, axis=1))
    return (_ta - _te) <= timedelta(tw)     


@jit(nopython=True)
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
        default=-99999, default_str="NotAvailable"):
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
        self.reserved_cols = []
        self.reserved_cols_index = []
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
        self.reserved_cols = self.conf.get("reserve", []) 
        self.reserved_cols_index = [self.col_index[k] for k in self.reserved_cols]
        self.primary_key = self.conf.get("index")
        self.key_index = [self.col_index[k] for k in self.conf.get("index")]

    def export_feature_dict(self):
        time_window = self.conf.get("time_window") if "time_window" in self.conf else [None]
        filter = self.conf.get("filters") if "filters" in self.conf else [None]
        name, cn_name = [], []
        for tw in time_window:
            _tw, _cn_tw = "", ""
            _tw = "" if tw is None else _tw + "".join(["last", str(tw), "days"])
            _cn_tw = "" if tw is None else _cn_tw + "".join(["过去", str(tw), "days"])

            for f in filter:
                fn    = f.get("name") if f is not None else ""
                fn_cn = f.get("cn_name") if f is not None else ""
                fn    = "__".join([ _tw, fn]) if _tw != "" else fn
                fn_cn = "__".join([ _tw, fn_cn]) if _tw != "" else fn_cn

                for fe_entry in self.conf.get("feature_entries"):
                    _pnm    = "__".join([ fn, fe_entry.get("prefix")])
                    _pnm_cn = "__".join([ fn_cn, fe_entry.get("desc")])
                    for f in fe_entry.get("aggregator"):
                        name.append("_".join([_pnm, f.__name__]))
                        cn_name.append("_".join([_pnm_cn, f.__doc__]))
        self.output_header = self.primary_key + self.reserved_cols + [self.domain + n if self.domain else n for n in name] 
        self.output_cn_header = self.primary_key + self.reserved_cols + [self.cn_domain + n if self.cn_domain else n for n in cn_name]

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

    def _compute(self, seq_no, vals):
        result = [v for v in np.take(vals, self.key_index + self.reserved_cols_index, axis=1)[0]]
        # Use `time_window` then combine with `filters` as criteria to select array data.
        time_window = self.conf.get("time_window") if "time_window" in self.conf else [None]
        for tw in time_window:
            tm_cond = _apply_timewindow(self.conf, self.col_index, tw, vals) if tw else np.array([True] * vals.shape[0])
            for f in self.conf.get("filters"):
                filter_idx = [ self.col_index[f] for f in f.get("feature") ]
                slim_filter_arr = np.take(vals, filter_idx, axis=1)
                filter_cond = apply_filter(func=f.get("func"), param=f.get("value"), arr=slim_filter_arr)

                combine_cond = tm_cond & filter_cond
                arr_ready = np.compress(combine_cond, vals, axis=0)

                for fe_entry in self.conf.get("feature_entries"):
                    _preprcss = fe_entry.get("preprocessor")
                    f_idx = [self.col_index[f] for f in fe_entry.get("feature")]
                    f_arr = np.take(arr_ready, f_idx, axis=1)
                    f_arr = _preprcss(f_arr)
                    print("[DEBUG] f_arr", f_arr)
                    _fn, _rslt = apply_agg(func=fe_entry.get("aggregator"), arr=f_arr)
                    for d in _rslt:
                        result.append(d)
        return seq_no, result