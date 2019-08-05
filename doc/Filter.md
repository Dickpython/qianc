
# Filter

Filter提供对特征输入数据的多次过滤操作，使用一次filter会相当于对原始数据应用了一次filter条件，通过filter条件后的数据会再进行接下来的计算。

### equal

过滤相当条件数值
~~~~~~~
"filters": [{
        "feature": ["QUERIER"], 
        "value": ["中国建设银行"], 
        "func": [equal],
        "cn_name": "中国建行",
        "name": "CCB",
     }]
~~~~~~~

### not_equal

过滤不相当条件数值
~~~~~~~
"filters": [{
        "feature": ["QUERIER"], 
        "value": ["中国建设银行"], 
        "func": [equal],
        "cn_name": "非中国建行",
        "name": "NotCCB",
     }]
~~~~~~~

### match

过滤字符串匹配的数值
~~~~~~~
"filters": [{
        "feature": ["QUERIER"], 
        "value": ["银行"], 
        "func": [match],
        "cn_name": "银行",
        "name": "Bank",
     }]
~~~~~~~


### not_match
过滤字符串不匹配的数值
~~~~~~~
"filters": [{
        "feature": ["QUERIER"], 
        "value": ["银行"], 
        "func": [not_match],
        "cn_name": "非银行",
        "name": "NotBank",
     }]
~~~~~~~

### parse_all
全匹配
~~~~~~~
"filters": [{
        "feature": ["QUERIER"], 
        "value": [""], 
        "func": [parse_all],
        "cn_name": "全部",
        "name": "All",
     }]
~~~~~~~

### regex_match
过滤正则匹配的数值; "value"中填入相应的正则表达式，当正则匹配返回True则选取该数值记录。
~~~~~~~
"filters": [{
        "feature": ["TYPE"], 
        "value": ["汽车|其他|农户|助学|经营"], 
        "func": [regex_match],
        "cn_name": "其他贷款",
        "name": "Otherloan",
    }]
~~~~~~~