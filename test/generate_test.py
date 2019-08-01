import sys
import unittest
sys.path.append('../../')

import fraudfeature as ftool
from fraudfeature import parse_float, parse_str, day_interval
from fraudfeature import equal, regex_match
from fraudfeature import Sum, Mean, DummyCount


class generate_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/test.tsv"
        self.result = "./output/result_test.tsv"
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
                    "value": ["c"], 
                    "func": [equal],
                    "cn_name": "过滤C",
                    "name": "filterC",
                },
                # {
                #     "feature": ["TYPE_C"], 
                #     "value": ["a|j"], 
                #     "func": [regex_match],
                #     "cn_name": "过滤AC",
                #     "name": "filterAC",
                # },
            ],
            "feature_entries":[
                {
                    "feature": ["CNT1"],
                    "prefix": "Cnt1",
                    "desc": "个数1",
                    "preprocessor": parse_float,
                    "aggregator": [Sum, Mean,],
                },
                {
                    "feature":["TYPE_C"],
                    "prefix": "TypeC",
                    "desc":"分类C",
                    "preprocessor": parse_str,
                    "aggregator":[DummyCount,],
                    "param":{"abcde":"C1", "defgh":"C2", "fghij":"C3", "klmno":"C4"}
                },
                {
                    "feature":["APPLY_DT", "EVENT_DT"],
                    "prefix": "ApplydtEventdt_Interval",
                    "desc":"分类C",
                    "preprocessor": day_interval,
                    "aggregator":[Sum,],
                }
            ]
        }
    
    def test_generate_process(self):
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf,
            domain = 'test.',
            cn_domain = '测试.'
        )
        
