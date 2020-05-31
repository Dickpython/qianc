import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import regex_match, day_interval, year_interval, parse_ratio, parse_float
from fraudfeature import DummyCount
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std


class yh_identity_test(unittest.TestCase):
    def setUp(self):
        self.path   = "./data/loan_data.tsv"
        self.result = "./output/loan_data_result.tsv"
        self.MONTH = 30
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "time_index": {"apply_dt": "ECREDDATE", "event_dt": "OPENDATE"},
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
                    "prefix": "State", "desc": "状态",
                    "aggregator": [DummyCount,],
                    "param":{ "NotAvailable":"C0",
                        "205|呆账": "C1",
                        "206|结清": "C2",
                        "5|转出": "C3",
                        "203|逾期": "C4",
                        "202|正常": "C5",
                    }
                },
                {
                    "feature": ["PAYMENTCYC"], 
                    "prefix": "Pymtcyc", "desc": "还款期数",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]
                },
                {
                    "feature": ["CREDITLIMITAMOUNT"], 
                    "prefix": "Creditlimitamt", "desc": "合同金额",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]
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
                        "4|信用/免担保":"C8",
                    }
                },
                {
                    "feature": ["PAYMENTRATING"], 
                    "prefix": "Pymtrating", "desc": "还款频率",
                    "aggregator": [DummyCount,],
                    "param":{ "NotAvailable":"C0",
                        "99|其他":"C1",
                        "02|周":"C2",
                        "03|月":"C3",
                        "01|日":"C4",
                        "07|一次性":"C5",
                        "06|年":"C6",
                        "04|季":"C7",
                        "08|不定期":"C8",
                    }
                },
                {
                    "feature":["ECREDDATE","OPENDATE"],
                    "prefix": "ApplydtOpendt_Interval", "desc": "贷款发放日期差",
                    "preprocessor": day_interval,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["ECREDDATE","ENDDATE"],
                    "prefix": "ApplydtEnddt_Interval", "desc": "贷款到期日期差",
                    "preprocessor": day_interval,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },

                {
                    "feature": ["CURROVERDUEAMOUNT"], 
                    "prefix": "Curodueamt", "desc": "当前逾期金额",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["CURROVERDUECYC"], 
                    "prefix": "Curroduecyc", "desc": "当前逾期期数",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["OVERDUE31TO60AMOUNT"], 
                    "prefix": "Odue31to60amt", "desc": "逾期31-60天未归还贷款本金",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["OVERDUE61TO90AMOUNT"], 
                    "prefix": "Odue61to90amt", "desc": "逾期61-90天未归还贷款本金",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["OVERDUE91TO180AMOUNT"], 
                    "prefix": "Odue91to180amt", "desc": "逾期91-180天未归还贷款本金",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },
                {
                    "feature": ["OVERDUEOVER180AMOUNT"], 
                    "prefix": "Odueover180amt", "desc": "逾期180天以上未归还贷款本金",
                    "preprocessor": parse_float,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,]  
                },

                {
                    "feature":["CURROVERDUEAMOUNT", "CREDITLIMITAMOUNT"], 
                    "prefix": "CurrodueamtCreditlimit_Ratio", "desc":"当前逾期金额占比",
                    "preprocessor": parse_ratio,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["OVERDUE31TO60AMOUNT", "CREDITLIMITAMOUNT"], 
                    "prefix": "Odue31to60amtCreditlimit_Ratio", "desc":"逾期31-60天未归还贷款本金占比",
                    "preprocessor": parse_ratio,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["OVERDUE61TO90AMOUNT", "CREDITLIMITAMOUNT"], 
                    "prefix": "Odue61to90amtCreditlimit_Ratio", "desc":"逾期61-90天未归还贷款本金占比",
                    "preprocessor": parse_ratio,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["OVERDUE91TO180AMOUNT", "CREDITLIMITAMOUNT"], 
                    "prefix": "Odue91to180amtCreditlimit_Ratio", "desc":"逾期91-180天未归还贷款本金占比",
                    "preprocessor": parse_ratio,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["OVERDUEOVER180AMOUNT", "CREDITLIMITAMOUNT"], 
                    "prefix": "Odueover180amtCreditlimit_Ratio", "desc":"逾期180天以上未归还贷款本金占比",
                    "preprocessor": parse_ratio,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["BALANCE"], 
                    "prefix": "Balance", "desc":"本金余额",
                    "preprocessor": parse_float,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["REMAINPAYMENTCYC"], 
                    "prefix": "Remainpycyc", "desc":"剩余还款期数",
                    "preprocessor": parse_float,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["SCHEDULEDPAYMENTAMOUNT"], 
                    "prefix": "Schedulepayamt", "desc":"本月应还款",
                    "preprocessor": parse_float,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["ACTUALPAYMENTAMOUNT"], 
                    "prefix": "Actualpayamt", "desc":"本月实还款",
                    "preprocessor": parse_float,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["CLASS5STATE"], 
                    "prefix": "Class5type", "desc":"五级分类",
                    "aggregator":[DummyCount,],
                    "param":{ "NotAvailable":"C0",
                        "1|正常":"C1",
                        "5|损失":"C2",
                        "3|次级":"C3",
                        "2|关注":"C4",
                        "4|可疑":"C5",
                        "9|未知":"C6",
                    }
                },
                {
                    "feature":["ECREDDATE","STATEENDDATE"],
                    "prefix": "ApplydtStateenddt_Interval", "desc": "状态截止日",
                    "preprocessor": year_interval,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["ECREDDATE","RECENTPAYDATE"],
                    "prefix": "ApplydtRecentpaydt_Interval", "desc": "最近一次还款日日期差",
                    "preprocessor": year_interval,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["SCHEDULEDPAYMENTDATE","RECENTPAYDATE"],
                    "prefix": "SchedulepaydtRecentpydt_Interval", "desc": "最近一次还款日期与应还款日期差",
                    "preprocessor": year_interval,
                    "aggregator": [Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["BALANCE", "CREDITLIMITAMOUNT"], 
                    "prefix": "BalanceCreditlimit_Ratio", "desc":"本金余额占比",
                    "preprocessor": parse_ratio,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["ACTUALPAYMENTAMOUNT", "SCHEDULEDPAYMENTAMOUNT"], 
                    "prefix": "ActualpayamtSchedulepayamt_Ratio", "desc":"本月实还款占应还款占比",
                    "preprocessor": parse_ratio,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
                {
                    "feature":["REMAINPAYMENTCYC", "PAYMENTCYC"], 
                    "prefix": "RemainpycycPycyc_Ratio", "desc":"剩余还款期数占比",
                    "preprocessor": parse_ratio,
                    "aggregator":[Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std,],
                },
            ]
        }
    
    def test_loan_process(self):
        print("[Exec] YH.LOAN ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = [None, '\\N', '',-99999.],
            domain = 'YH.LOAN.',
            cn_domain = '人行.贷款.'
        )
        
