import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import equal
from fraudfeature import parse_ratio, month_interval
from fraudfeature import PassThrough


class yh_overduesummary_test(unittest.TestCase):
    def setUp(self):
        # self.path   = "./data/overduesum_data.tsv"
        # self.result = "./output/overduesum_data_result.tsv"
        self.path   = "./test/data/overduesum_data.tsv"
        self.result = "./test/output/overduesum_data_result.tsv"
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],

            "filters": [
                {
                    "feature": ["TYPE"], 
                    "value": ["0001"], 
                    "func": [equal],
                    "cn_name": "贷款",
                    "name": "Loan",
                },
                {
                    "feature": ["TYPE"], 
                    "value": ["0002"], 
                    "func": [equal],
                    "cn_name": "贷记卡",
                    "name": "Lc",
                },
                {
                    "feature": ["TYPE"], 
                    "value": ["0003"], 
                    "func": [equal],
                    "cn_name": "准贷记卡",
                    "name": "Slc",
                },
            ],
            
            "feature_entries":[
                {
                    "feature":["COUNT"],
                    "prefix": "Overduecnt", "desc": "逾期笔数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["MAXDURATION"],
                    "prefix": "Maxoduemon", "desc": "逾期最长月数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["MONTHS"],
                    "prefix": "Months", "desc": "逾期月份数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["HIGHESTOVERDUEAMOUNTPERMON"],
                    "prefix": "Monmaxodueamt", "desc": "逾期单月最高总额",
                    "aggregator":[PassThrough,],
                },
            ]
        }
    
    def test_overduesummary_process(self):
        print("[Exec] YH.OVERDUESUMMARY ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = ['\\N', '', '--'],
            domain = 'YH.OVERDUESUMMARY.',
            cn_domain = '人行.逾期信息汇总.'
        )
        
