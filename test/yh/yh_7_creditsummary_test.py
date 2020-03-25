import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import parse_ratio, month_interval
from fraudfeature import PassThrough


class yh_creditsummary_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/creditsumm_data.tsv"
        self.result = "./output/creditsumm_data_result.tsv"
        # self.path   = "./test/data/creditsumm_data.tsv"
        # self.result = "./test/output/creditsumm_data_result.tsv"
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            
            "feature_entries":[
                {
                    "feature":["LOANCARDCOUNT"],
                    "prefix": "Loancardcount",
                    "desc":"贷记卡账户数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["STANDARDLOANCARDCOUNT"],
                    "prefix": "Stdloancardcount", "desc": "准贷记卡账户数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["PERHOUSELOANCOUNT"],
                    "prefix": "Perhouseloancnt", "desc": "个人住房贷款笔数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["PERBUSINESSHOUSELOANCOUNT"],
                    "prefix": "Perbusinesshouseloancnt", "desc": "个人商用房贷款笔数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["OTHERLOANCOUNT"],
                    "prefix": "Otherloancnt", "desc": "其他贷款笔数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["PERHOUSELOANCOUNT", "OTHERLOANCOUNT"],
                    "prefix": "PerhouseloancntOtherloancnt_Ratio", "desc": "住房贷款其他贷款账户数比例",
                    "preprocessor": parse_ratio,
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["LOANCARDCOUNT", "STANDARDLOANCARDCOUNT"],
                    "prefix": "LoancardcntStdloancardcnt_Ratio", "desc": "贷记卡准贷记卡账户数比例",
                    "preprocessor": parse_ratio,
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["ECREDDATE", "FIRSTLOANOPENMONTH"],
                    "prefix": "ApplydtFirstloanopmon_Interval", "desc": "首笔贷款发放时间差",
                    "preprocessor": month_interval,
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["ECREDDATE", "FIRSTLOANCARDOPENMONTH"],
                    "prefix": "ApplydtFirstloancardopmon_Interval", "desc": "首张贷记卡发放时间差",
                    "preprocessor": month_interval,
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["ECREDDATE", "FIRSTSTANDARDLOANCARDOPENMONTH"],
                    "prefix": "ApplydtFirststdloancardopmon_Interval", "desc": "首张准贷记卡发放时间差",
                    "preprocessor": month_interval,
                    "aggregator":[PassThrough,],
                },
            ]
        }
    
    def test_creditsummary_process(self):
        print("[Exec] YH.CREDITSUMMARYCUE ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = ['\\N', '', '--'],
            domain = 'YH.CREDITSUMMARYCUE.',
            cn_domain = '人行.信用汇总.'
        )
        
