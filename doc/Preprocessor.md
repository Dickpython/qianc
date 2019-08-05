# Preprocessor

预处理函数的使用在Filter函数使用之后。预处理函数本身并不是必须的步骤，只有当现有的数据字段无法满足特征衍生需求时，才需要使用使用预处理函数对现在字段进行一次加工，如：时间的标准化、计算不同字段间的比例、截取地址信息、计算字符串相似度等等。


### parse_normal_time
单字段预处理函数，将时间字段的字符串转化城datetime对象


### parse_float
单字段预处理函数，将字符串的字段转化城float对象

### day_interval
双字段预处理函数，计算两个时间字符串之间的日期差，返回int对象。如为missing value返回默认无效值⚠️不完整的时间字符会被补全到1日或者1月1日。

### month_interval
双字段预处理函数，计算两个时间字符串之间的月份差，返回int对象。如为missing value返回默认无效值 ⚠️不完整的时间字符会被补全到1日或者1月1日。

### year_interval
双字段预处理函数，计算两个时间字符串之间的年份差，返回int对象。如为missing value返回默认无效值 ⚠️不完整的时间字符会被补全到1日或者1月1日。

### parse_ratio
双字段预处理函数，计算两个数值字符之间的比例，如为missing value返回默认无效值；如字符转换数值失败则返回默认无效值。

### cal_similarity
双字段预处理函数，计算两个字符串之间的Levenstain Distance Score，如字符为missing value则返回默认无效值。

### parse_region
单字段预处理函数，获取地址字符串对应的区域信息，返回String。


### parse_city
单字段预处理函数，获取地址字符串对应的城市信息，返回String。

### parse_citytier
单字段预处理函数，获取地址字符串对应的城市等级信息，返回String。

### parse_24month
单字段预处理函数，针对人行过去24个月状态的字符串，对字符串中"N","1","2","3","*",...等等每一个状态值做统计，返回一个numpy.array对象，该对象记录param中定义的每一个字符的个数。
