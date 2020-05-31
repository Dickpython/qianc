
import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
import pandas as pd
from fraudfeature import regex_match, day_interval,month_interval,year_interval, parse_24month
from fraudfeature import DummyCount, PassThrough
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75



class prepro_time_interval_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/time_test.tsv"
        self.result = "./output/result_time_test.tsv"
        self.conf = {
            "index" : ["ID","FLAG"],
            # "time_index" : {"apply_dt": "APPLY_DT", "event_dt": "EVENT_DT"},
            "feature_entries":[
                {
                    "feature":["APPLY_DT", "EVENT_DT"],
                    "prefix": "ApplydtEventdt_Interval",
                    "desc":"全部",
                    "preprocessor": year_interval,
                    "aggregator":[Sum,Max,Min],
                },
                {
                    "feature":["APPLY_DT", "STATE_END_DT"],
                    "prefix": "AppStEddt_Interval",
                    "desc":"全部",
                    "preprocessor": year_interval,
                    "aggregator":[Sum,Max,Min],
                }
            ]
        }
    
    def test_generate_process(self):
        ftool.generate(
            raw = self.path, 
            chunksize=10,
            result_file_path = self.result,
            # missing_value=[-99999.],
            conf = self.conf,
            domain = 'test.',
            cn_domain = '测试.'
        )
        