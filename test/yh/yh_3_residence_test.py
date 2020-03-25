import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import day_interval
from fraudfeature import parse_region, parse_city, parse_citytier
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std
from fraudfeature import DummyCount, UniqueCount


class yh_residence_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/residence_data.tsv"
        self.result = "./output/residence_data_result.tsv"
        # self.path   = "./test/data/residence_data.tsv"
        # self.result = "./test/output/residence_data_result.tsv"
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "feature_entries":[
                {
                    "feature":["RESIDENCETYPE"],
                    "prefix": "Residencetype",
                    "desc":"居住状态",
                    "aggregator":[DummyCount,],
                    "param":{"NotAvailable":"C0",
                        "50|租房":"C1", 
                        "99|其他":"C2", 
                        "30|亲属楼宇":"C3", 
                        "40|集体宿舍":"C4",
                        "99|未知":"C5",
                        "60|共有住宅":"C6",
                        "10|自置": "C7",
                        "20|按揭": "C8"},

                },
                {
                    "feature":["ADDRESS"],
                    "prefix": "Addr_Region",
                    "desc":"居住地址区域",
                    "aggregator":[DummyCount,],
                    "param":{
                        "NotAvailable":"C0",
                        "东北": "C1",
                        "华东":"C2",
                        "华中":"C3",
                        "华北":"C4",
                        "华南":"C5",
                        "西北":"C6",
                        "西南":"C7",
                    }
                },
                {
                    "feature":["ADDRESS"],
                    "prefix": "Addr_Citys",
                    "preprocessor": parse_city,
                    "desc":"居住所在城市",
                    "aggregator":[UniqueCount,]
                },
                {
                    "feature":["ADDRESS"],
                    "prefix": "Addr_Citytier",
                    "preprocessor": parse_citytier,
                    "desc":"居住城市等级",
                    "aggregator":[DummyCount,],
                    "param":{
                        "NotAvailable":"C0",
                        "T1": "C1",
                        "T2a":"C2",
                        "T2b":"C3",
                        "T3":"C4",
                        "T4-":"C5",
                    }
                },
                {
                    "feature":["ECREDDATE", "GETTIME"],
                    "prefix": "ApplyGettime_Interval",
                    "preprocessor": day_interval,
                    "desc":"居住信息更新时间差",
                    "aggregator":[Quantile25, Quantile75, Max, Min, Mean, Sum, Median, Std], 
                },
            ]
        }
    
    def test_residence_process(self):
        print("[Exec] YH.RESIDENCE ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = ['\\N', ''],
            domain = 'YH.RESIDENCE.',
            cn_domain = '人行.居住信息.'
        )
        
