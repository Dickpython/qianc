import numpy as np
from multiprocessing import Pool
from datetime import datetime
from dateutil.parser import parse
from itertools import product


def parse_date(date_str, dayfirst=False):
    date_str = date_str.split('.')[0] if len(date_str)>20 else date_str.replace('.','-')
    # to-do: dt.year need to be updated！
    try:
        dt = parse(date_str, fuzzy=True, dayfirst=dayfirst)
        return dt
    except ValueError:
        try:
            dt = datetime.fromtimestamp(int(date_str))
            if dt.year > 1900 and dt.year < 9999:
                return dt
            else:
                return None
        except ValueError:
            return None


def PassThrough(vals, default=np.nan):
    if vals is None or vals.shape[0] == 0:
        return default 
    return vals[0]


def DiffYear(date_tuple, default=np.nan):
    date_1, date_2 = date_tuple[0], date_tuple[1]
    dt1 = parse_date(date_1)
    dt2 = parse_date(date_2)
    if dt1 and dt2: 
        return np.array([dt1.year - dt2.year])
    return np.array([default])


def __enumerate_group(sequence, keyfunc):
    last_pk, n = None, 0
    elem_batch = []
    for elem in sequence:
        primary_key = "".join(keyfunc(elem))
        if primary_key and primary_key != last_pk:
            yield n, elem_batch
            n += 1
            elem_batch = [] 
            last_pk = primary_key
        elem_batch.append(elem)
    yield n, elem_batch


class Conf:
    def __init__(self, path, conf, sep='\t', domain=None, cn_domain=None):
        self.conf = conf
        self.domain = domain
        self.cn_domain = cn_domain
        self.output_header = None
        self.output_cn_header = None
        self.key_index = []
        self.primary_key = None
        self.time_index_id = []
        self.col_index = {}
        self.index_col = {}
        self.sep = sep
        if self.check_conf():
            self._load_index(path)
        else:
            pass
            # logger.Error invalid! 
 
    def check_conf(self):
        if "index" in self.conf and len(self.conf.get("index"))>0 :
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

    def apply_key(self, vals):
        val = vals.decode().strip("\n").split(self.sep)
        return [val[i] for i in self.key_index]

    {% block pipefunc%}
    
    {% endblock %}

{% block main%}

{% endblock %}
    