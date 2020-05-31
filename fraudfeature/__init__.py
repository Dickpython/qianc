import os

from multiprocessing import Pool
import time
from datetime import datetime
from tqdm import tqdm
from .conf import Conf
from .filter import equal, not_equal, regex_match, parse_all, match, not_match
from .aggregator import PassThrough, Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std, UniqueCount
from .aggregator import DummyCount, MulMax, MulMin, MulSum, MulMean, MulStd, MulQuantile25, MulQuantile75, MulMedian, MulQuantile
from .preprocessor import parse_float, parse_str, day_interval, month_interval, year_interval
from .preprocessor import cal_similarity, parse_24month, parse_ratio
from .preprocessor import parse_region, parse_city, parse_citytier, parse_merge


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


def generate(raw=None, result_file_path=None, conf=None, 
        n=1, chunksize=1, debug=False, log_enable=False, log_path=None, 
        sep='\t', domain=None, cn_domain=None, 
        missing_value=[],default=-99999., default_str="NotAvailable", default_time=datetime(1900,1,1)):
    if raw is None and os.path.exists(raw) is False:
        print("[ERROR] Input file not exists!")
        # log.Error raw file path not exists.
        return 
    if os.path.exists("/".join(result_file_path.split('/')[:-1])) is False:
        print("[ERROR] Output file not exists!")
        # log.Error result file path not exists
        return
    config = Conf(path=raw, conf=conf, sep=sep, domain=domain, 
    cn_domain=cn_domain, missing_value=missing_value,
    default=default, default_str=default_str) 
    if config.valid is False:
        # log.Error configuration is invalid
        print("[ERROR] configuration is invalid!")
        return

    output_header = config.output_header
    if output_header is None or len(output_header) == 0:
        # loger.Info header is invalid!
        print("[INFO] header is invalid!")
        output_header = ""
    # log.Info, log key_index
    feature_dict_path = ".".join(result_file_path.split('.')[:-1]) + "_cnmap.tsv"

    pool = Pool(n)
    with open(raw, "rb") as input_file, open(result_file_path, "w") as output_file, open(feature_dict_path, "w") as cnmap_file:
        for e, c in zip(output_header, config.output_cn_header):
            if e not in config.primary_key:
                cnmap_file.write(e + '\t' + c + '\n')
        output_file.write(sep.join(output_header) + '\n')
        #output_file.write(sep.join(config.output_cn_header) + '\n')
        # skip header
        input_file.readline()
        for seq_no, out_data in pool.imap(config.pipefunc, \
            tqdm(__enumerate_group(input_file, config.apply_key), desc="Process"), chunksize=chunksize):
            if seq_no == 0:
                continue
            output_file.write(sep.join([str(v) for v in out_data]) + "\n")
    return 0


def check():
    pass
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
