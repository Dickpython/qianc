import sys
import unittest
sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import regex_match, day_interval, equal, parse_float
from fraudfeature import DummyCount, PassThrough
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std


class yh_specialtrade_test(unittest.TestCase):
    def setUp(self):
        # self.path   = "./data/specialtrade_data.tsv"
        # self.tmp = "./output/specialtrade_data_result_1.tsv"
        # self.tmp_cnmap = "./output/specialtrade_data_result_1_cnmap.tsv"
        # self.result = "./output/specialtrade_data_result.tsv"
        self.path   = "./test/data/specialtrade_data.tsv"
        self.tmp = "./test/output/specialtrade_data_result_1.tsv"
        self.tmp_cnmap = "./test/output/specialtrade_data_result_1_cnmap.tsv"
        self.result = "./test/output/specialtrade_data_result.tsv"
        self.MONTH = 30
        
        self.conf_1 = {
            "index" : ["CONTNO", "SUPER_ID"],
            "filters": [
                {
                    "feature": ["BUSINESSTYPE"], 
                    "value": ["房"], "func": [regex_match],  "cn_name": "住房贷款",  "name": "Houseloan",
                },
                {
                    "feature": ["BUSINESSTYPE"], 
                    "value": ["消费"], "func": [regex_match],  "cn_name": "消费贷款",  "name": "Consloan",
                },
                {
                    "feature": ["BUSINESSTYPE"], 
                    "value": ["汽车|其他|农户|助学|经营"], "func": [regex_match], "cn_name": "其他贷款", "name": "Otherloan",
                },
                {
                    "feature": ["BUSINESSTYPE"], 
                    "value": ["0002"], "func": [equal], "cn_name": "贷记卡", "name": "Lc",
                },
                {
                    "feature": ["BUSINESSTYPE"], 
                    "value": ["0003"], "func": [equal], "cn_name": "准贷记卡", "name": "Slc",
                },
            ],
            "feature_entries":[
                {
                    "feature": ["TYPE"],
                    "prefix": "Type",
                    "desc": "特殊交易类型",
                    "aggregator": [DummyCount,],
                    "param": {"NotAvailable": "C0",
                        "9|其他": "C1",
                        "2|担保人代还": "C2",
                        "1|展期（延期）": "C3",
                        "5|提前还款（全部）": "C4",
                        "4|提前还款（部分）": "C5",
                        "3|以资抵债": "C6",
                        }
                },
                {
                    "feature": ["CHANGINGMONTHS"],
                    "prefix": "Changemon",
                    "desc": "特殊交易变化月数",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]
                },
                {
                    "feature": ["CHANGINGAMOUNT"],
                    "prefix": "Changeamt",
                    "desc": "特殊交易变化金额",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]
                },
            ]
        }
    
    def test_loan_process(self):
        print("[Exec] YH.SPECIALTRADE STAGE 1 ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.tmp,
            conf = self.conf_1, 
            missing_value = [None, '\\N', ''],
            domain = '',
            cn_domain = ''
        )

        fltr_map = {}
        with open(self.tmp_cnmap, 'r') as cnmap_file:
            for l in cnmap_file.readlines():
                k, v = l.strip('\n').split('\t')
                fltr_map[k] = v

        feature_entries = []
        for k, n in fltr_map.items():
            _cnf = { "feature": [k],
                "preprocessor": parse_float,
                "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                "prefix": k,
                "desc": n,
            }
            feature_entries.append(_cnf) 

        # self.conf_2 = {
        #     "index": ["CONTNO"],
        #     "feature_entries": feature_entries,
        # }

        # ftool.generate(
        #     raw = self.tmp, 
        #     result_file_path = self.result,
        #     conf = self.conf_2, 
        #     missing_value = ['-99999', None, '\\N', ''],
        #     domain = 'YH.SPECIALTRADE.',
        #     cn_domain = '人行.特殊交易.'
        # )
        
