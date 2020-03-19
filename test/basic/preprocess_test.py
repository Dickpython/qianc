import sys
import unittest
sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import Sum, Mean
from fraudfeature import parse_merge



class preprocessor_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/test.tsv"
        self.result = "./output/result_merge_test.tsv"
        self.conf = {
            "index" : ["ID","FLAG"],
            "time_index" : {"apply_dt": "APPLY_DT", "event_dt": "EVENT_DT"},
            "feature_entries":[
                {
                    "feature": ["CNT1","CNT2"],
                    "prefix": "Cnt1_cnt2_merge",
                    "desc": "个数1_个数2",
                    "preprocessor": parse_merge,
                    "aggregator": [Sum, Mean,],
                }
            ]
        }
    
    def test_preprocessor_process(self):
        ftool.generate(
            raw = self.path,
            result_file_path = self.result,
            conf = self.conf,
            domain = 'test.',
            cn_domain = '测试.',
            missing_value=['']
        )
