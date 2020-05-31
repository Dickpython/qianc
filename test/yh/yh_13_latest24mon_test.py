import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import regex_match, day_interval, parse_24month
from fraudfeature import DummyCount, PassThrough
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75
from fraudfeature import MulSum, MulMax, MulMin, MulMedian, MulStd, MulQuantile


class yh_identity_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/past24mon_data.tsv"
        self.result = "./output/past24mon_data_result.tsv"
        self.MONTH = 30
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "time_index": {"apply_dt": "ECREDDATE" , "event_dt": "OPENDATE"},
            "time_window": [self.MONTH *3, self.MONTH *6, self.MONTH *12, self.MONTH *12*3, self.MONTH *12*5 ],
            "filters": [
                {
                    "feature": ["TYPE"], 
                    "value": ["房"], "func": [regex_match],  "cn_name": "住房贷款",  "name": "Houseloan",
                },
                {
                    "feature": ["TYPE"], 
                    "value": ["消费"], "func": [regex_match],  "cn_name": "消费贷款",  "name": "Consloan",
                },
                {
                    "feature": ["TYPE"], 
                    "value": ["汽车|其他|农户|助学|经营"], "func": [regex_match], "cn_name": "其他贷款", "name": "Otherloan",
                },
            ],
            "feature_entries":[
                {
                    "feature": ["LATEST24STATE"],
                    "prefix": "State",
                    "desc": "状态",
                    "preprocessor":parse_24month,
                    "aggregator": [MulQuantile,],
                    "param": {'N':'C1', '1':'C2', '*':'C3', '2':'C4', '/':'C5', '#':'C6', 'C':'C7',
                        '3':'C8', '4':'C9', '5':'C10', '6':'C11', '7':'C12', 'D':'C13', 'G':'C14'}
                },
            ]
        }
    
    def test_loan_process(self):
        print("[Exec] YH.24MONTHSTATE ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = [None, '\\N', ''],
            domain = 'YH.24MONTHSTATE.',
            cn_domain = '人行.过去24个月还款状态.'
        )
        
