import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import regex_match, day_interval, year_interval, parse_ratio, parse_float
from fraudfeature import DummyCount
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std


class yh_loancard_test(unittest.TestCase):
    def setUp(self):
        # self.path   = "./data/loancard_data.tsv"
        # self.result = "./output/loancard_data_result.tsv"
        self.path   = "./test/data/loancard_data.tsv"
        self.result = "./test/output/loancard_data_result.tsv"
        self.MONTH = 30
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "time_index": {"apply_dt": "ECREDDATE", "event_dt": "OPENDATE"},
            "time_window": [self.MONTH *3, self.MONTH *6, self.MONTH *12, self.MONTH *12*3, self.MONTH *12*5 ],

            "feature_entries":[
                {
                    "feature": ["STATE"], 
                    "prefix": "State", "desc": "状态",
                    "aggregator": [DummyCount,],
                    "param":{ "NotAvailable":"C0",
                        "3|止付": "C6",
                        "5|呆帐": "C7",
                        "2|冻结": "C8",
                        "1|正常": "C9",
                        "809|销户": "C10",
                        "803|未激活": "C11",
                    }
                },
                {
                    "feature": ["CURRENCY"], "prefix": "Currency", "desc": "币种",
                    "aggregator": [DummyCount,],
                    "param":{ "NotAvailable": "C0",
                        "欧元": "C1",
                        "美元": "C2",
                        "澳大利亚元": "C3",
                        "港元": "C4",
                        "英镑": "C5",
                        "人民币": "C6",
                    }
                },
                {
                    "feature": ["FINANCETYPE"], 
                    "prefix": "Finorg", "desc": "贷款机构",
                    "aggregator": [DummyCount,],
                    "param":{ "NotAvailable":"C0",
                        "外资银行":"C1",
                        "机构":"C2",
                        "住房公积金管理中心":"C3",
                        "汽车金融公司":"C4",
                        "村镇银行":"C5",
                        "商业银行":"C6",
                        "财务公司":"C7",
                        "住房储蓄银行":"C8",
                        "小额信贷公司":"C9",
                        "金融租赁公司":"C10",
                        "消费金融有限公司":"C11",
                        "信托投资公司":"C12",
                    }
                },
                {
                    "feature": ["GUARANTEETYPE"], 
                    "prefix": "Guranteetype", "desc": "担保方式",
                    "aggregator": [DummyCount,],
                    "param":{ "NotAvailable":"C0",
                        "9|其他":"C1",
                        "5|组合（含保证）":"C2",
                        "1|质押（含保证金）":"C3",
                        "6|组合（不含保证）":"C4",
                        "7|农户联保":"C5",
                        "2|抵押":"C6",
                        "3|保证":"C7",
                        "4|信用/免担保":"C8"
                    }
                },
                {
                    "feature": ["CREDITLIMITAMOUNT"], 
                    "prefix": "Creditlimitamt", "desc": "授信额度",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]
                },
                {
                    "feature": ["CURROVERDUEAMOUNT"], 
                    "prefix": "Curodueamt", "desc": "当前逾期金额",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["SHAREDCREDITLIMITAMOUNT"], 
                    "prefix": "Sharelimitamt", "desc": "共享额度",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["USEDCREDITLIMITAMOUNT"], 
                    "prefix": "Usedamt", "desc": "已用额度",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["LATEST6MONTHUSEDAVGAMOUNT"], 
                    "prefix": "Last6mavgusedamt", "desc": "最近6个月平均使用额度",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["USEDHIGHESTAMOUNT"], 
                    "prefix": "Maxusedamt", "desc": "最大使用额度",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["ACTUALPAYMENTAMOUNT"], 
                    "prefix": "Actualamt", "desc": "本月实还款",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["SCHEDULEDPAYMENTAMOUNT"], 
                    "prefix": "Scheduleamt", "desc": "本月应还款",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature":["ECREDDATE","STATEENDDATE"],
                    "prefix": "ApplydtStateenddt_Interval", "desc": "状态截止日期差",
                    "preprocessor": day_interval,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["ECREDDATE","RECENTPAYDATE"],
                    "prefix": "ApplydtRecentpaydt_Interval", "desc": "最近一次还款日期差",
                    "preprocessor": day_interval,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["RECENTPAYDATE","SCHEDULEDPAYMENTDATE"],
                    "prefix": "RecentpydtSchedulepydt_Interval", "desc": "最近一次还款与账单日期差",
                    "preprocessor": day_interval,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["LATEST6MONTHUSEDAVGAMOUNT", "CREDITLIMITAMOUNT"],
                    "prefix": "Last6monavgamtCreditlimit_Ratio", "desc": "最近6个月平均使用额度占比",
                    "preprocessor": parse_ratio,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["ACTUALPAYMENTAMOUNT", "CREDITLIMITAMOUNT"],
                    "prefix": "ActpyamtCreditlimit_Ratio", "desc": "本月实还款占比",
                    "preprocessor": parse_ratio,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["USEDHIGHESTAMOUNT", "CREDITLIMITAMOUNT"],
                    "prefix": "UsedmaxamtCreditlimit_Ratio", "desc": "最大使用额度占比",
                    "preprocessor": parse_ratio,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["USEDCREDITLIMITAMOUNT", "CREDITLIMITAMOUNT"],
                    "prefix": "UsdcreditamtCreditlimit_Ratio", "desc": "已用额度占比",
                    "preprocessor": parse_ratio,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["ACTUALPAYMENTAMOUNT", "SCHEDULEDPAYMENTAMOUNT"],
                    "prefix": "ActualpayamtSchedulepayamt_Ratio", "desc": "本月实还款应还款占比",
                    "preprocessor": parse_ratio,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature": ["CURROVERDUECYC"], 
                    "prefix": "Curroduecyc", "desc": "当前逾期期数",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature":["CURROVERDUEAMOUNT", "CREDITLIMITAMOUNT"],
                    "prefix": "CurrodueamtCreditlimit_Ratio", "desc": "当前逾期金额占比",
                    "preprocessor": parse_ratio,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
            ]
        }
    
    def test_loancard_process(self):
        print("[Exec] YH.LOANCARD ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = [None, '\\N', ''],
            domain = 'YH.LOANCARD.',
            cn_domain = '人行.贷记卡.'
        )
        
