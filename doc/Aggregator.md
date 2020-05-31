# Aggregator

Aggregator是特征衍生最后进行聚合、统计计算的函数。


## Basic Aggregator

### PassThrough
直接透传数据，仅支持传非array数据.
PassThrough的默认值，默认使用default_str,当preprocessor为parse_float时default value为numeric的default

### Count
对一组数据进行个数计算，去除missing_value.

### UniqueCount
对一组数据进行去重个数计算，暂时不去除missing_value.

### Sum
对一组数据进行数值累和计算，去除missing_value.

### Max
对一组数据进行数最大值计算，去除missing_value.

### Min
对一组数据进行数最小值计算，去除missing_value.

### Mean
对一组数据进行数平均值计算，去除missing_value.

### Std
对一组数据进行标准差计算，去除missing_value.

### Median
对一组数据进行中位数计算，去除missing_value.

### Quantile25
对一组数据进行percentil计算，取25分位数，去除missing_value.

### Quantile75
对一组数据进行percentil计算，取75分位数，去除missing_value.


## Advanced Aggregator

### DummyCount
对一组数据中指定的某些特定值进行计数统计，去除missing_value.

### MulMax
对一组二维数据进行统计，计算列维度上的每一组值的最大值。

### MulSum
对一组二维数据进行统计，计算列维度上的每一组值的累和值。

### MulMin
对一组二维数据进行统计，计算列维度上的每一组值的最小值。

### MulMean
对一组二维数据进行统计，计算列维度上的每一组值的平均值。

### MulStd
对一组二维数据进行统计，计算列维度上的每一组值的方差值。

### MulQuantile25
对一组二维数据进行统计，计算列维度上的每一组值的25分位数。

### MulQuantile75
对一组二维数据进行统计，计算列维度上的每一组值的75分位数。

### MulMedian
对一组二维数据进行统计，计算列维度上的每一组值的中位数。
