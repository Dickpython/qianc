import sys
import unittest
# sys.path.append('../../../')

import fraudfeature as ftool
from fraudfeature import day_interval
from fraudfeature import parse_region
from fraudfeature import Mean, Sum, Max, Min, Median, Quantile25, Quantile75, Std
from fraudfeature import DummyCount, UniqueCount, PassThrough


class yh_recordsummary_test(unittest.TestCase):
    def setUp(self):
        # self.path   = "./data/recordsumm_data.tsv"
        # self.result = "./output/recordsumm_data_result.tsv"
        self.path   = "./test/data/recordsumm_data.tsv"
        self.result = "./test/output/recordsumm_data_result.tsv"
        
        self.conf = {
            "index" : ["CONTNO","FLAG"],
            "feature_entries":[
                {
                    "feature":["CCARCY1EMIENQRINSTNUM"],
                    "prefix": "Ccarcy1emienqrinstnum",
                    "desc":"信用卡审批最近1个月内的查询机构数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["LNAPRVRCY1EMIEINSTNUM"],
                    "prefix": "Lnaprvrcy1emieinstnum",
                    "desc":"贷款审批最近1个月内的查询机构数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["LNAPRVRCLY1EMIENQRCNT"],
                    "prefix": "Lnaprvrcly1emienqrcnt",
                    "desc":"贷款审批最近1个月内的查询次数",
                    "aggregator":[PassThrough,]
                },
                {
                    "feature":["CCARCY1EMINNRSENQRCNT"],
                    "prefix": "Ccarcy1eminnrsenqrcnt",
                    "desc":"信用卡审批最近1个月内的查询次数",
                    "aggregator":[PassThrough,],
                },
                {
                    "feature":["MYSLFENQRR1EMIENQRCNT"],
                    "prefix": "Myslfenqrr1emienqrcnt",
                    "desc":"本人查询最近1个月内的查询次数",
                    "aggregator":[PassThrough,], 
                },
                {
                    "feature":["PSTLOANMGTR2YIENQRCNT"],
                    "prefix": "Pstloanmgtr2yienqrcnt",
                    "desc":"贷后管理最近2年内的查询次数",
                    "aggregator":[PassThrough,], 
                },
                {
                    "feature":["WRNTQUAEXMR2YIENQRCNT"],
                    "prefix": "Wrntquaexmr2yienqrcnt",
                    "desc":"担保资格审查最近2年内的查询次数",
                    "aggregator":[PassThrough,], 
                },
                {
                    "feature":["APNTMRCHRNER2YIENRCNT"],
                    "prefix": "Apntmrchrner2yienrcnt",
                    "desc":"特约商户实名审查最近2年内的查询次数",
                    "aggregator":[PassThrough,], 
                },
            ]
        }
    
    def test_recordsummary_process(self):
        print("[Exec] YH.RECORDSUMMARY ...")
        ftool.generate(
            raw = self.path, 
            result_file_path = self.result,
            conf = self.conf, 
            missing_value = ['\\N', ''],
            domain = 'YH.RECORDSUMMARY.',
            cn_domain = '人行.查询汇总.'
        )
        
