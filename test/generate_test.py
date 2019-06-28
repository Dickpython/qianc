import sys
import unittest
sys.path.append('../../')

import fraudfeature as ftool
from fraudfeature import parse_float
from fraudfeature import equal, regex_match
from fraudfeature import sum, avg


class generate_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./test.tsv"
        self.result = "./result_test.tsv"
        self.conf = {
            "index" : ["ID"],
            "reserve" : ["FLAG"],
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
                    "aggregator": [sum, avg],
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
        
