import sys
import unittest
sys.path.append('../../')

import fraudfeature as ftool
from fraudfeature import year_interval, parse_str, parse_region
from fraudfeature import parse_all, regex_match
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75
from fraudfeature import PassThrough, DummyCount


class yh_profession_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/recorddeta_data.tsv"
        self.result = "./output/recorddeta_data_result.tsv"
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "filters": [
                {
                    "feature": ["QUERIER"], 
                    "value": [""], 
                    "func": [parse_all],
                    "cn_name": "全类型",
                    "name": "All",
                },
                {
                    "feature": ["QUERIER"], 
                    "value": ["建设银行"], 
                    "func": [regex_match],
                    "cn_name": "本行查询",
                    "name": "Selfcheck",
                },
            ],
            "feature_entries":[
                {
                    "feature":["QUERYREASON"],
                    "prefix": "Queryreason",
                    "desc":"查询",
                    "aggregator":[DummyCount,],
                    "param":{"NotAvailable":"C0",
                         "08|担保资格审查": "C1",
                        "03|信用卡审批": "C2",
                        "02|贷款审批": "C3"},

                },
            ]
        }
    
    def test_profession_process(self):
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = ['\\N', ''],
            domain = 'YH.RECORDINFO.',
            cn_domain = '人行.征信查询明细信息.'
        )
        
