import sys
import unittest
sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import parse_float, parse_str, day_interval
from fraudfeature import equal, regex_match
from fraudfeature import Sum, Mean, DummyCount


class filter_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/test.tsv"
        self.result = "./output/result_filter_test.tsv"
        self.conf = {
            "index" : ["ID","FLAG"],
            "time_index" : {"apply_dt": "APPLY_DT", "event_dt": "EVENT_DT"},
            "filters": [
                {
                    "feature": ["TYPE"], 
                    "value": ["a"], 
                    "func": [equal],
                    "cn_name": "过滤A",
                    "name": "filterA",
                },
                {
                    "feature": ["TYPE"], 
                    "value": ["x"], 
                    "func": [equal],
                    "cn_name": "过滤X",
                    "name": "filterX",
                },
            ],
            "feature_entries":[
                {
                    "feature": ["CNT1"],
                    "prefix": "Cnt1",
                    "desc": "个数1",
                    "preprocessor": parse_float,
                    "aggregator": [Sum,],
                },
            ]
        }
    
    def test_generate_process(self):
        ftool.generate(
            raw = self.path, 
            chunksize=10,
            result_file_path = self.result,
            conf = self.conf,
            domain = 'test.',
            cn_domain = '测试.'
        )
        
