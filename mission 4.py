
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 重新加载数据
df = pd.read_csv('ICData.csv', sep=',')
df['交易时间'] = pd.to_datetime(df['交易时间'])
df['hour'] = df['交易时间'].dt.hour
df['minute'] = df['交易时间'].dt.minute
df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])
df = df[df['ride_stops'] != 0]

# 筛选上车刷卡记录
df_boarding = df[df['刷卡类型'] == 0].copy()

print("=" * 70)
print("任务4: 高峰小时系数 (PHF) 计算")
print("=" * 70)

# ==================== 步骤1: 高峰小时识别 ====================
print("\n" + "=" * 70)
print("步骤1: 高峰小时识别")
print("=" * 70)

# 统计全天各小时刷卡量
hourly_counts = df_boarding.groupby('hour').size()
hourly_counts = hourly_counts.reindex(range(24), fill_value=0)

print("\n全天各小时刷卡量分布:")
for h in range(24):
    print(f"  {h:02d}:00 - {h+1:02d}:00: {hourly_counts[h]:5d} 次")

# 找出高峰小时
peak_hour = hourly_counts.idxmax()
peak_hour_count = hourly_counts.max()

print(f"\n>>> 高峰小时识别结果:")
print(f"高峰小时为 {peak_hour:02d}:00-{peak_hour+1:02d}:00，刷卡量 {peak_hour_count} 次")


# ==================== 步骤2: 5分钟粒度统计 ====================
print("\n" + "=" * 70)
print("步骤2: 5分钟粒度统计")
print("=" * 70)

# 筛选高峰小时的数据
peak_hour_data = df_boarding[df_boarding['hour'] == peak_hour].copy()

# 以"08:00-09:00"样式打印筛选结果
print(f"\n高峰小时 ({peak_hour:02d}:00-{peak_hour+1:02d}:00) 共有 {len(peak_hour_data)} 条记录")

# 创建5分钟时间窗口标签
# 将分钟映射到5分钟区间 (0-4, 5-9, 10-14, ..., 55-59)
peak_hour_data['minute_5'] = (peak_hour_data['minute'] // 5) * 5 #整数除法实现"向下取整"，再乘5得到区间起点

# 统计每个5分钟窗口的刷卡量
five_min_counts = peak_hour_data.groupby('minute_5').size()
five_min_counts = five_min_counts.reindex(range(0, 60, 5), fill_value=0)

# 打印各5分钟窗口的统计结果，循环遍历12个时间段
print("\n高峰小时内各5分钟窗口刷卡量:")
for m in range(0, 60, 5):
    count = five_min_counts[m]
    print(f"  {peak_hour:02d}:{m:02d} - {peak_hour:02d}:{m+5:02d}: {count:4d} 次")

# 找出最大5分钟刷卡量
max_5min_count = five_min_counts.max() # 获取12个区间中的最大值
max_5min_start = five_min_counts.idxmax() # 获取最大值对应的区间起点（0/5/10...）
max_5min_end = max_5min_start + 5 # 计算区间终点（起点+5分钟）

# 打印最大5分钟区间的统计结果
print(f"\n>>> 最大5分钟刷卡量: {max_5min_count} 次")
print(f"    时间段: {peak_hour:02d}:{max_5min_start:02d} ~ {peak_hour:02d}:{max_5min_end:02d}")

# 计算PHF5
PHF5 = peak_hour_count / (12 * max_5min_count)
print(f"\n>>> PHF5 计算:")
print(f"PHF5 = {peak_hour_count} / (12 × {max_5min_count}) = {PHF5:.4f}")


# ==================== 步骤3: 15分钟粒度统计 ====================
print("\n" + "=" * 70)
print("步骤3: 15分钟粒度统计")
print("=" * 70)

# 创建15分钟时间窗口标签 (0-14, 15-29, 30-44, 45-59)
peak_hour_data['minute_15'] = (peak_hour_data['minute'] // 15) * 15

# 统计每个15分钟窗口的刷卡量
fifteen_min_counts = peak_hour_data.groupby('minute_15').size()
fifteen_min_counts = fifteen_min_counts.reindex([0, 15, 30, 45], fill_value=0)

# 打印各15分钟窗口的统计结果，循环遍历4个时间段
print("\n高峰小时内各15分钟窗口刷卡量:")
for m in [0, 15, 30, 45]:
    count = fifteen_min_counts[m]
    end_m = m + 15
    print(f"  {peak_hour:02d}:{m:02d} - {peak_hour:02d}:{end_m:02d}: {count:4d} 次")

# 找出最大15分钟刷卡量
max_15min_count = fifteen_min_counts.max()
max_15min_start = fifteen_min_counts.idxmax()
max_15min_end = max_15min_start + 15

print(f"\n>>> 最大15分钟刷卡量: {max_15min_count} 次")
print(f"    时间段: {peak_hour:02d}:{max_15min_start:02d} ~ {peak_hour:02d}:{max_15min_end:02d}")

# 计算PHF15
PHF15 = peak_hour_count / (4 * max_15min_count)
print(f"\n>>> PHF15 计算:")
print(f"PHF15 = {peak_hour_count} / (4 × {max_15min_count}) = {PHF15:.4f}")


# ==================== 步骤4: 最终输出 ====================
print("\n" + "=" * 70)
print("任务4: 最终输出结果")
print("=" * 70)

# 格式化输出
print(f"\n高峰小时：{peak_hour:02d}:00 ~ {peak_hour+1:02d}:00，刷卡量：{peak_hour_count} 次")
print(f"\n最大5分钟刷卡量（{peak_hour:02d}:{max_5min_start:02d}~{peak_hour:02d}:{max_5min_end:02d}）：{max_5min_count} 次")
print(f"PHF5  = {peak_hour_count} / (12 × {max_5min_count}) = {PHF5:.4f}")
print(f"\n最大15分钟刷卡量（{peak_hour:02d}:{max_15min_start:02d}~{peak_hour:02d}:{max_15min_end:02d}）：{max_15min_count} 次")
print(f"PHF15 = {peak_hour_count} / ( 4 × {max_15min_count}) = {PHF15:.4f}")

print("\n" + "=" * 70)
print("PHF 指标解读:")
print("=" * 70)
print(f"PHF5  = {PHF5:.4f} (越接近1表示高峰小时内客流越均匀)")
print(f"PHF15 = {PHF15:.4f} (越接近1表示高峰小时内客流越均匀)")
print(f"\n通常PHF15 > PHF5，因为15分钟窗口平滑了更多波动")
print(f"本结果: PHF15({PHF15:.4f}) > PHF5({PHF5:.4f}) ✓ 符合预期")
