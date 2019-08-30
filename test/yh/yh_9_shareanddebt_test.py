import sys
import unittest
sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import equal
from fraudfeature import parse_ratio, month_interval
from fraudfeature import PassThrough


class yh_overduesummary_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/shareanddeb_data.tsv"
        self.result = "./output/shareanddeb_data_result.tsv"
        
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
                    "feature":["FINANCECORPCOUNT"],
                    "prefix": "Fincorpcnt", "desc": "法人机构数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["ACCOUNTCOUNT"],
                    "prefix": "Acccount", "desc": "账户数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["CREDITLIMIT"],
                    "prefix": "Creditlimit", "desc": "总授信金额",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["BALANCE"],
                    "prefix": "Balance", "desc": "余额",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["USEDCREDITLIMIT"],
                    "prefix": "Usedamt", "desc": "已用金额",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["LATEST6MONTHUSEDAVGAMOUNT"],
                    "prefix": "Last6monavgusedamt", "desc": "最近6个月平均已用金额",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["MAXCREDITLIMITPERORG"],
                    "prefix": "Maxcredit", "desc": "最高授信金额",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["MINCREDITLIMITPERORG"],
                    "prefix": "Mincredit", "desc": "最低授信金额",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["LATEST6MONTHUSEDAVGAMOUNT", "CREDITLIMIT"],
                    "prefix": "Last6musedamtCredit_Ratio", "desc": "过去6个月已用金额占比",
                    "preprocesssor": parse_ratio,
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["USEDCREDITLIMIT", "CREDITLIMIT"],
                    "prefix": "UsedcreditCreditlimit_Ratio", "desc": "已用金额占比",
                    "preprocesssor": parse_ratio,
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["BALANCE", "CREDITLIMIT"],
                    "prefix": "BalanceCreditlimit_Ratio", "desc": "余额占比",
                    "preprocesssor": parse_ratio,
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["CREDITLIMIT", "ACCOUNTCOUNT"],
                    "prefix": "CreditlimitAccnt_Ratio", "desc": "平均账户授信总额",
                    "preprocesssor": parse_ratio,
                    "aggregator":[PassThrough,],
                },
            ]
        }
    
    def test_shareanddebt_process(self):
        print("[Exec] YH.SHAREANDDEBT ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = ['\\N', '', '--'],
            domain = 'YH.OVERDUESUMMARY.',
            cn_domain = '人行.逾期信息汇总.'
        )
        
