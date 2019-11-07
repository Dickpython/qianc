import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import parse_all, regex_match, day_interval
from fraudfeature import PassThrough


class yh_creditscore_test(unittest.TestCase):
    def setUp(self):
        # self.path   = "./data/creditscore_data.tsv"
        # self.result = "./output/creditscore_data_result.tsv"
        self.path   = "./test/data/creditscore_data.tsv"
        self.result = "./test/output/creditscore_data_result.tsv"
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            
            "feature_entries":[
                {
                    "feature":["SCORE"],
                    "prefix": "Score",
                    "desc":"信用分",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["SCORELEVEL"],
                    "prefix": "Scorelvl", "desc": "相对位置",
                    "aggregator":[PassThrough,],
                },
            ]
        }
    
    def test_creditscore_process(self):
        print("[Exec] YH.CREDITSCORE ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = ['\\N', '', '--'],
            domain = 'YH.CREDITSCORE.',
            cn_domain = '人行.征信评分.'
        )
        
