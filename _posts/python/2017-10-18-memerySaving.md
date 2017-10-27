---
layout: post
title: pandas-DataFrame 内存节省方略
date: 2017-10-18
author: xiaoyongsheng
categories: Python
tag: Python

---

* content
{: toc}

---

- 获取 DataFrame 数据量/数据类型/内存使用量信息

```
df.info(memory_usage="deep")  # memory_usage: 是否精确显示内存使用量
```

- 转换字段类型


memory  usage | float | int | uint | datetime | bool | object
-                       | -         | -         | -    | -                 | -         | - 
1  bytes        |              -  |  int8 | uint8 |-        |  bool |  
2  bytes        | float16 | int16 | uint16 | 
4  bytes        | float32 | int32 | uint32 | 
8  bytes        | float64 | int64 | uint64 | datetime64 |  | 
variable     | -           | -         | -             | -                     |  object


```
# 查看字段类型的表达范围
np.iinfo("int32")

# 选择相同类型的字段
cvt = df.select_dtypes(include=['int'])

# 多列转换为数值型字段
cvt.apply(pd.to_numeric, downcast="signed")  # downcast: signed / unsigned / float

# 离散字段存储方式
df['col'].astype('category') # 当 nunique / total <= 0.5 时采用

converted_obj = pd.DataFrame()

for col in gl_obj.columns:
    num_unique_values = len(gl_obj[col].unique())
    num_total_values = len(gl_obj[col])
    if num_unique_values / num_total_values < 0.5:
        converted_obj.loc[:,col] = gl_obj[col].astype('category')
    else:
        converted_obj.loc[:,col] = gl_obj[col]


# 在读取 csv 文件时，以字典的方式指定读取的字段类型
column_types = {
   'acquisition_info': 'category',
    'h_caught_stealing': 'float32',
    'h_player_1_name': 'category'
}
read_and_optimized = pd.read_csv('game_logs.csv',dtype=column_types,parse_dates=['date'],infer_datetime_format=True)

```

## 参考资料  

[^1]: Using pandas with large data. (2017). Data Science Blog: Dataquest. Retrieved 18 October 2017, from https://www.dataquest.io/blog/pandas-big-data/
