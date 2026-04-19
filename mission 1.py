
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 设置中文显示
plt.rcParams['figure.figsize'] = (12, 8)

# ==================== 任务1: 数据预处理 ====================

# 1. 读取数据
print("=" * 60)
print("任务1.1: 读取数据")
print("=" * 60)

# 读取CSV文件，注意分隔符为制表符
df = pd.read_csv('ICData.csv', sep=',')

# 打印前5行
print("数据集前5行:")
print(df.head())

# 打印基本信息
print(f"\n数据集基本信息:")
print(f"行数: {df.shape[0]}")
print(f"列数: {df.shape[1]}")
print(f"\n各列数据类型:")
print(df.dtypes)
print(f"\n列名: {list(df.columns)}")


# 2. 时间解析
print("\n" + "=" * 60)
print("任务1.2: 时间解析")
print("=" * 60)

# 将交易时间转换为datetime类型
df['交易时间'] = pd.to_datetime(df['交易时间'])

# 提取小时字段
df['hour'] = df['交易时间'].dt.hour


# 3. 构造衍生字段 - 搭乘站点数
print("\n" + "=" * 60)
print("任务1.3: 构造衍生字段 ride_stops")
print("=" * 60)

# 计算搭乘站点数 (|下车站点 - 上车站点|)
df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])

print(f"ride_stops列构造成功!")

# 检查ride_stops为0的记录数
zero_stops = df[df['ride_stops'] == 0]
zero_count = len(zero_stops)
print(f"\nride_stops为0的记录数: {zero_count}")

# 删除异常记录
if zero_count > 0:
    df = df[df['ride_stops'] != 0]
    print(f"已删除 {zero_count} 条异常记录")
    print(f"剩余记录数: {len(df)}")
else:
    print("未发现ride_stops为0的记录")


# 4. 缺失值检查
print("\n" + "=" * 60)
print("任务1.4: 缺失值检查")
print("=" * 60)

# 检查各列缺失值数量
missing_counts = df.isnull().sum()
print("各列缺失值数量:")
print(missing_counts)

# 总缺失值数
total_missing = df.isnull().sum().sum()
print(f"\n总缺失值数: {total_missing}")

# 如果有缺失值，进行处理
if total_missing > 0:
    print("\n处理策略:")
    for col in df.columns: #逐列检查每一列
        if df[col].isnull().sum() > 0: #该列是否有缺失值
            missing_count = df[col].isnull().sum()  #统计该列缺失值数量
            if df[col].dtype in ['int64', 'float64']: #判断是否为数值型
                #策略：数值型用中位数填充（抗异常值干扰）
                median_val = df[col].median() #取该列中位数
                df[col].fillna(median_val, inplace=True) #原地填充
                print(f"  - {col}: {missing_count}个缺失值，用中位数({median_val})填充")
            else:
                #策略：非数值型用众数填充
                mode_val = df[col].mode()[0] #取该列众数（第1个）
                df[col].fillna(mode_val, inplace=True)  #原地填充
                print(f"  - {col}: {missing_count}个缺失值，用众数({mode_val})填充")

    print(f"\n处理后缺失值数量:")
    print(df.isnull().sum()) #验证缺失值是否已全部处理
else:
    print("\n未发现缺失值，无需处理")

print("\n" + "=" * 60)
print("数据预处理完成!")
print("=" * 60)
print(f"最终数据集信息:")
print(f"行数: {df.shape[0]}")
print(f"列数: {df.shape[1]}")
print(f"\n最终列名: {list(df.columns)}")

