import sys
import unittest
sys.path.append('../../')

import fraudfeature as ftool
from fraudfeature import year_interval, parse_str
from fraudfeature import parse_region, cal_similarity
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75
from fraudfeature import PassThrough, DummyCount


class yh_profession_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/profession_data.tsv"
        self.result = "./output/profession_data_result.tsv"
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "feature_entries":[
                {
                    "feature":["DUTY"],
                    "prefix": "Duty",
                    "desc":"职务",
                    "aggregator":[DummyCount,],
                    "param":{"NotAvailable":"C0",
                        "99|未知":"C1", 
                        "30|一般员工":"C2", 
                        "20|中级领导（行政级别局级以下领导或大公司中级管理人员）":"C3", 
                        "10|高级领导（行政级别局级及局级以上领导或大公司高级管理人员）":"C4",
                        "98|其他":"C5"},

                },
                {
                    "feature":["TITLE"],
                    "prefix": "Title",
                    "desc":"职称",
                    "aggregator":[DummyCount,],
                    "param":{"NotAvailable":"C0",
                        "04|无":"C1", 
                        "03|初级":"C2", 
                        "02|中级":"C3", 
                        "01|高级":"C4"},
                },
                {
                    "feature":["INDUSTRY"],
                    "prefix": "Industry",
                    "desc":"行业",
                    "aggregator":[DummyCount,],
                    "param":{
                        "NotAvailable":"C0",
                        "I000000000|住宿和餐饮业": "C1",
                        "T000000000|国际组织":"C2",
                        "K000000000|房地产业":"C3",
                        "C000000000|制造业":"C4",
                        "B000000000|采掘业":"C5",
                        "R878720000|文化、体育和娱乐业":"C6",
                        "P840000000|教育":"C7",
                        "E000000000|建筑业":"C8",
                        "G000000000|信息传输、计算机服务和软件业":"C9",
                        "O000000000|居民服务和其他服务业":"C10",
                        "L000000000|租赁和商务服务业":"C11",
                        "S000000000|公共管理和社会组织":"C12",
                        "A000000000|农、林、牧、渔业":"C13",
                        "J000000000|金融业":"C14",
                        "N000000000|水利、环境和公共设施管理业":"C15",
                        "Q000000000|卫生、社会保障和社会福利业":"C16",
                        "H000000000|批发和零售业":"C17",
                        "F000000000|交通运输、仓储和邮政业":"C18",
                        "D000000000|电力、煤气及水的生产和供应业":"C19",
                        "M000000000|科学研究、技术服务业和地质勘察业":"C20",
                    }
                },
                {
                    "feature":["OCCUPATION"],
                    "prefix": "Occupation",
                    "desc":"职业",
                    "aggregator":[DummyCount,],
                    "param":{
                        "NotAvailable": "C0",
                        "1100|军人": "C1",
                        "0500|农、林、牧、渔、水利业生产人员": "C2",
                        "0400|商业、服务业人员": "C3",
                        "0100|专业技术人员": "C4",
                        "0390|办事人员和有关人员": "C5",
                        "1200|不便分类的其它从业人员": "C6",
                        "0600|生产、运输设备操作人员及有关人员": "C7",
                        "0000|国家机关、党群组织、企业、事业单位负责人": "C8",
                    }
                },
                {
                    "feature":["ECREDDATE", "STARTYEAR"],
                    "prefix": "EcredtStartyear_Interval",
                    "preprocessor": year_interval,
                    "desc":"工作起始时间时间差",
                    "aggregator":[Quantile25, Quantile75, Max, Min, Mean, Sum, Median],#  
                },
                {
                    "feature":["ECREDDATE", "GETTIME"],
                    "prefix": "EcredtGettime_Interval",
                    "preprocessor": year_interval,
                    "desc":"工作信息更新时间差",
                    "aggregator":[Quantile25, Quantile75, Max, Min, Mean, Sum, Median],#  
                },
                {
                    "feature": ["EMPLOYERADDRESS"],
                    "preprocessor": parse_region,
                    "prefix": "Employeraddr_Region",
                    "desc": "单位地址区域",
                    "aggregator": [DummyCount,],
                    "param":{
                        "NotAvailable": "C0",
                        "东北": "C1",
                        "华东": "C2",
                        "华中": "C3",
                        "华北": "C4",
                        "华南": "C5",
                        "西北": "C6",
                        "西南": "C7",
                    }
                },

            ]
        }
    
    def test_profession_process(self):
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = ['\\N', ''],
            domain = 'YH.PROFESSION.',
            cn_domain = '人行.职业信息.'
        )
        
