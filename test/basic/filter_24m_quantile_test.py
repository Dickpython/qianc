import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
import pandas as pd
from fraudfeature import regex_match, day_interval, parse_24month
from fraudfeature import DummyCount, PassThrough
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75
from fraudfeature import MulSum, MulMax, MulMin, MulMedian, MulStd, MulQuantile, MulMean


class filter_24m_quantile_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/past24mon_data.tsv"
        self.result = "./output/filter_24m_quantile_result.tsv"
        self.MONTH = 30
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "time_index": {"apply_dt": "ECREDDATE" , "event_dt": "OPENDATE"},
            "time_window": [self.MONTH *12*3],
            "filters": [
                {
                    "feature": ["TYPE"], 
                    "value": ["房"], "func": [regex_match],  "cn_name": "住房贷款",  "name": "Houseloan",
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
                    "aggregator": [MulQuantile],
                    "param": {'N':'C1','*':'C3'}

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
        r = pd.read_csv(self.result, sep='\t')
        assert len(r.columns) == 14
        assert len(r) == 3
        assert r[r['CONTNO']==110006315600781748]['YH.24MONTHSTATE.Houseloan__Last1080Days__State_C1_MulQuantile25'].values[0]==-99999.
        assert r[r['CONTNO']==110006315600782905]['YH.24MONTHSTATE.Houseloan__Last1080Days__State_C1_MulQuantile25'].values[0]==-99999.
        assert r[r['CONTNO']==110006315600782905]['YH.24MONTHSTATE.Otherloan__Last1080Days__State_C1_MulQuantile75'].values[0]==3.0
        assert r[r['CONTNO']==110006315600782905]['YH.24MONTHSTATE.Otherloan__Last1080Days__State_C3_MulQuantile75'].values[0]==20.0
        assert r[r['CONTNO']==110006315600782906]['YH.24MONTHSTATE.Otherloan__Last1080Days__State_C1_MulQuantile75'].values[0]==0.0
        
