import sys
import unittest
sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import regex_match, day_interval, parse_ratio
from fraudfeature import DummyCount
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75


class yh_identity_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/loan_data.tsv"
        self.result = "./output/loan_data_result.tsv"
        self.MONTH = 30
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "time_index": {"apply_dt": "ECREDDATE" , "event_dt": "OPENDATE"},
            "time_window": [self.MONTH *3, self.MONTH *6, self.MONTH *12, self.MONTH *12*3, self.MONTH *12*5 ],
            "filters": [
                {
                    "feature": ["TYPE"], 
                    "value": ["房"], 
                    "func": [regex_match],
                    "cn_name": "住房贷款",
                    "name": "Houseloan",
                },
                {
                    "feature": ["TYPE"], 
                    "value": ["消费"], 
                    "func": [regex_match],
                    "cn_name": "消费贷款",
                    "name": "Consloan",
                },
                {
                    "feature": ["TYPE"], 
                    "value": ["汽车|其他|农户|助学|经营"], 
                    "func": [regex_match],
                    "cn_name": "其他贷款",
                    "name": "Otherloan",
                },
            ],
            "feature_entries":[
                {
                    "feature": ["STATE"],
                    "prefix": "State",
                    "desc": "状态",
                    "aggregator": [DummyCount,],
                    "param":{"NotAvailable":"C0",
                        "205|呆账": "C1",
                        "206|结清": "C2",
                        "5|转出": "C3",
                        "203|逾期": "C4",
                        "202|正常": "C5",
                        }
                },
                {
                    "feature": ["CURRENCY"],
                    "prefix": "Currency",
                    "desc": "币种",
                    "aggregator": [DummyCount,],
                    "param":{"NotAvailable": "C0",
                        "欧元": "C1",
                        "美元": "C2",
                        "澳大利亚元": "C3",
                        "港元": "C4",
                        "英镑": "C5",
                        "人民币": "C6",
                    }
                },
                {
                    "feature":["CURROVERDUEAMOUNT", "CREDITLIMITAMOUNT"],
                    "prefix": "CurrodueamtCreditlimit_Ratio",
                    "preprocessor": parse_ratio,
                    "desc":"当前逾期金额占比",
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75,],
                },
            ]
        }
    
    def test_loan_process(self):
        print("[Exec] YH.LOAN ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = [None, '\\N', ''],
            domain = 'YH.LOAN.',
            cn_domain = '人行.贷款.'
        )
        
