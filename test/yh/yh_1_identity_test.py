import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import year_interval, parse_str, parse_city,parse_region,parse_citytier
from fraudfeature import equal, regex_match,cal_similarity
from fraudfeature import PassThrough, DummyCount, UniqueCount


class yh_1_identity_test(unittest.TestCase):
    def setUp(self):
        # self.path   = "./data/identity_data.tsv"
        # self.result = "./output/identity_data_result.tsv"
        self.path   = "./data/identity_data.tsv"
        self.result = "./output/identity_data_result.tsv"
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "feature_entries":[
                {
                    "feature": ["ECREDDATE", "BIRTHDAY"],
                    "prefix": "Age",
                    "desc": "年龄",
                    "preprocessor": year_interval,
                    "aggregator": [PassThrough,],
                },
                {
                    "feature":["GENDER"],
                    "prefix": "Gender",
                    "desc":"性别",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["EDUDEGREE"],
                    "prefix": "Edudegree",
                    "desc":"学位",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["EDULEVEL"],
                    "prefix": "Edulevel",
                    "desc":"学历",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["MARITALSTATE"],
                    "prefix": "Marital",
                    "desc":"婚姻状况",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["REGISTEREDADDRESS", "POSTADDRESS"],
                    "prefix": "RegisteraddPostaddress_Similarity",
                    "preprocessor": cal_similarity,
                    "desc":"户籍通讯录地址匹配度",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["POSTADDRESS"],
                    "prefix": "Area_City",
                    "preprocessor": parse_city,
                    "desc":"户籍通地址城市",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["REGISTEREDADDRESS"],
                    "prefix": "Area_Region",
                    "preprocessor": parse_region,
                    "desc":"户籍通地址城市",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["POSTADDRESS"],
                    "prefix": "Area_CityTier",
                    "preprocessor": parse_citytier,
                    "desc":"户籍通地址城市",
                    "aggregator":[UniqueCount],
                    
                },
                {
                    "feature":["POSTADDRESS"],
                    "prefix": "Area_CityTier",
                    "preprocessor": parse_citytier,
                    "desc":"户籍通地址城市",
                    "aggregator":[DummyCount],
                    "param":{
                    "NotAvailable":"C0",
                    "T1":"C1",
                    "T2a": "C1",
                    "T2b": "C3",
                    "T3": "C4",
                    "T4-": "C5"
                    }
                }
            ]
        }
    
    def test_identity_process(self):
        print("[Exec] YH.IDENTITY ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = [None, '\\N', ''],
            domain = 'YH.IDENTITY.',
            cn_domain = '人行.身份信息.'
        )
        
