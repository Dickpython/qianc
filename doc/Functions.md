本文档是对fraudfeature工具的特征衍生函数进行详细的解读。

### fraudfeature::generate
~~~~~~~~~~
generate(raw=None, result_file_path=None, conf=None, n=1, chunksize=1, 
    debug=False, log_enable=False, log_path=None, sep='\t', domain=None, cn_domain=None, 
    missing_value=[],default=-99999.,default_str="NotAvailable")
~~~~~~~~~~

#### Params
- **raw**, string, 原始文件路径。
- **result_file_path**, string, 输出结果文件路径。
- **conf**, dict, 特征衍生配置字段。
- **n**, int, 指定并行个数，默认为1。
- **chunksize**, int, 使用并行时对调用数据指定chunksize，当数据量较大时，使用大的chunksize可以提高计算效率，默认值为1。
- **debug**, boolean, 启动debug模式，打印详细的日志，默认False。
- **log_enable**, boolean, 输出日志到文件开关，默认False。
- **log_path**, string, 输出日志路径。
- **sep**, string, 原始文件分隔符。
- **domain**, string, 特征Domain的英文前缀。
- **cn_domain**, string, 特征Domain的中文前缀。
- **missing_value**, list, 全局缺失值列举。
- **default**, float, 全局连续型默认值。
- **default_str**, string, 全局离散型默认值。