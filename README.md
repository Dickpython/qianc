# Introduction

人行特征衍生的工作经过多轮的迭代，特征逻辑以及原始数据的结构，已经相对成熟和稳定。所以将已知的人行特征衍生知识工程化，可以提升入场项目中对人行特征数据衍生的效率。

FraudFeature人行特征衍生工具，是对anti_fraud_sys老的特征脚本做了优化和更新，删除了冗余的逻辑和代码，修复了已知的问题后，增加了对特征运算的并行处理以及计算进度跟踪等功能。经过JH项目的测试，目前已经是一个稳定的版本，后续也计划根据FraudFeature版本再进行工程优化。


# Table of Content

- [Installation](##Installation)
- [Quick Test]
- [Usage](##Usage)
- [Example and Advance Usage]()
- [Document]()
  * [Functions](https://git.creditx.com/jh2019/fraudfeature/blob/master/doc/Functions.md)
  * [Filter](https://git.creditx.com/jh2019/fraudfeature/blob/master/doc/Filter.md#filter)
  * [Preprocessor](https://git.creditx.com/jh2019/fraudfeature/blob/master/doc/Preprocessor.md#preprocessor)
  * [Aggregator](https://git.creditx.com/jh2019/fraudfeature/blob/master/doc/Aggregator.md#aggregator)
    - [Basic](https://git.creditx.com/jh2019/fraudfeature/blob/master/doc/Aggregator.md#basic-aggregator)
    - [Advanced](https://git.creditx.com/jh2019/fraudfeature/blob/master/doc/Aggregator.md#advanced-aggregator)
- [FAQ & Known Issues](##FAQ\ and\ Known\ Issues)


## Installation

1. 直接到内部nexus.creditx.com中下载安装；
2. 或通过pip安装；
~~~~~~~~~~~~~~
pip install fraudfeature
~~~~~~~~~~~~~~
3. 或使用git clone代码到本地，本地引入使用；

## Quick Test

进入test目录，直接运行run_test.py检查FraudFeature测试用例是否通过
```
    cd ./test
    python run_test.py
```

## Usage

使用时引入 generate特征衍生函数 和 PassThrough算子函数
~~~~~~~~~~~~~~~~
> from fraudfeature import generate
> from fraudfeature import PassThrough
~~~~~~~~~~~~~~~~

指定特征衍生配置Json。
- "index" 指定文件的唯一标识字段。
- "features_entries" 指定文件特定的字段进行特征衍生。"feature" 为字段名称, "prefix" 是衍生特征的核心特征名缩写, desc是衍生特征的核心特征中文描述, aggregator是衍生特征需要使用的算子。
~~~~~~~~~~~~~~~~
> conf = {
    "index" : ["CONTNO","FLAG"],
    "feature_entries":[
        {
            "feature": ["LATEST24STATE"],
            "prefix": "State",
            "desc": "状态",
            "aggregator": [PassThrough,],
        },
    ]
}
~~~~~~~~~~~~~~~~

运行特征衍生函数。
~~~~~~~~~~~~~~~~
> generate(
    raw = "./test/data/past24mon_data.tsv", 
    result_file_path = "./test/output/past24mon_data_result.tsv",
    conf = conf, 
    missing_value = [None, '\\N', ''],
    domain = 'YH.24MONTHSTATE.',
    cn_domain = '人行.过去24个月还款状态.'
)
~~~~~~~~~~~~~~~~


## FAQ

#### Q1. 输入文件是否需要排序？
Answer: 需要，输入文件请按照唯一标识字段进行排序后，再使用特征衍生工具。

#### Q2. 如何并行地进行特征衍生？
Answer: 特征衍生函数generate中使用参数n，可以指定衍生特征的并行个数。默认n=1。

#### Q3. generate()函数中的默认值，使用有哪些注意事项？
Answer: fraudfeature默认值，主要是指当遇到无效输入和算子计算结果无效需要填充的默认值，定义为默认值。fraudfeature使用全局的默认值，即在generate(..)函数里可以定义全局的default，全局default根据算子的数据类型分为3类：

- 1）数值型的算子；
- 2）字符型的算子；
- 3）时间类型算子；

不同类型的算子，会默认自动应用default=-99999.0, default_str="NotAvailable", default_time=datetime(1900,1,1)。

#### Q4. PassThrough算子的默认值是怎样的？
Answer: PassThrough的默认值，默认使用default_str,当preprocessor为parse_float时default value为numeric的default

#### Q5. generate()函数中的missing_value，使用有哪些注意事项？
Answer: 
missing_value用来定义全局的缺失值，默认missing_value是一个包含None值的List，全局缺失值这处理时，对将missing_value列表中所有的值都当作是缺失处理，不参与运算。

因为fraudfeature所有的输入最初都会被当作str来读取，因此确实值都要使用引号包裹，尤其是在二次计算的domain中，上一级计算结果默认值'-99999.0',在下一级的missing_value中要添加上，否则-99999.0可能会参与计算，导致结果异常。
