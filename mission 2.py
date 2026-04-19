
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置中文显示
plt.rcParams['figure.figsize'] = (12, 8)

# 读取数据
df = pd.read_csv('ICData.csv', sep=',')
df['交易时间'] = pd.to_datetime(df['交易时间'])
df['hour'] = df['交易时间'].dt.hour
df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])
df = df[df['ride_stops'] != 0]  # 删除异常记录

print("数据重新加载完成!")
print(f"数据集形状: {df.shape}")


# ==================== 任务2: 时间分布分析 ====================
print("=" * 60)
print("任务2: 时间分布分析")
print("=" * 60)

# 筛选刷卡类型=0的记录（上车刷卡）
df_boarding = df[df['刷卡类型'] == 0].copy()
print(f"\n上车刷卡记录总数: {len(df_boarding)}")

# (a) 早晚时段刷卡量统计 - 使用numpy
print("\n" + "=" * 60)
print("任务2(a): 早晚时段刷卡量统计 (使用numpy)")
print("=" * 60)

# 提取hour列为numpy数组
hours = df_boarding['hour'].values

# 使用numpy布尔索引统计早峰前时段 (hour < 7)
early_mask = hours < 7
early_count = np.sum(early_mask)

# 使用numpy布尔索引统计深夜时段 (hour >= 22)
night_mask = hours >= 22
night_count = np.sum(night_mask)

# 计算百分比
total_count = len(df_boarding)
early_pct = (early_count / total_count) * 100
night_pct = (night_count / total_count) * 100

print(f"\n时段统计结果:")
print(f"早峰前时段 (hour < 7): {early_count} 次 ({early_pct:.2f}%)")
print(f"深夜时段 (hour >= 22): {night_count} 次 ({night_pct:.2f}%)")
print(f"全天总刷卡量: {total_count} 次")

# 验证：使用numpy.where实现相同功能
print(f"\n[numpy.where验证]")
early_where = np.sum(np.where(hours < 7, 1, 0))
night_where = np.sum(np.where(hours >= 22, 1, 0))
print(f"早峰前时段 (np.where): {early_where} 次")
print(f"深夜时段 (np.where): {night_where} 次")


# (b) 24小时刷卡量分布可视化
print("\n" + "=" * 60)
print("任务2(b): 24小时刷卡量分布可视化 (matplotlib)")
print("=" * 60)

# 统计每小时的刷卡量
hourly_counts = df_boarding.groupby('hour').size()
# 确保包含所有24小时（0-23）
hourly_counts = hourly_counts.reindex(range(24), fill_value=0)

print("\n24小时刷卡量分布:")
for h in range(24):
    print(f"  {h:02d}:00 - {hourly_counts[h]:5d} 次")

df_boarding = df[df['刷卡类型'] == 0].copy()

# 设置中文字体 - 使用系统中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 统计每小时刷卡量
hourly_counts = df_boarding.groupby('hour').size().reindex(range(24), fill_value=0)

# 创建颜色数组
bar_colors = []
for h in range(24):
    if h < 7:
        bar_colors.append('#E74C3C')  # 红色 - 早峰前
    elif h >= 22:
        bar_colors.append('#9B59B6')  # 紫色 - 深夜
    else:
        bar_colors.append('#3498DB')  # 蓝色 - 常规时段

# 创建图形
fig, ax = plt.subplots(figsize=(14, 8), dpi=150)

# 绘制柱状图
bars = ax.bar(range(24), hourly_counts.values, color=bar_colors, edgecolor='black', linewidth=0.5)

# 设置x轴
ax.set_xticks(range(0, 24, 2))
ax.set_xticklabels([f'{h}' for h in range(0, 24, 2)], fontsize=11)
ax.set_xlabel('小时 (Hour)', fontsize=14, fontweight='bold')

# 设置y轴
ax.set_ylabel('刷卡量 (次)', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(hourly_counts.values) * 1.15)

# 添加数值标签
for i, (h, count) in enumerate(hourly_counts.items()):
    if h % 2 == 0:
        ax.text(h, count + 200, str(count), ha='center', va='bottom', fontsize=8, rotation=90)

# 添加标题
ax.set_title('公交IC卡24小时刷卡量分布\n(早峰前时段<7时标红，深夜时段≥22时标紫)',
             fontsize=16, fontweight='bold', pad=20)

# 添加图例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#E74C3C', edgecolor='black', label='早峰前时段 (<7时)'),
    Patch(facecolor='#3498DB', edgecolor='black', label='常规时段 (7-21时)'),
    Patch(facecolor='#9B59B6', edgecolor='black', label='深夜时段 (≥22时)')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=11)

# 添加水平网格线
ax.grid(axis='y', linestyle='--', alpha=0.7)

# 添加垂直参考线
ax.axvline(x=6.5, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
ax.axvline(x=21.5, color='purple', linestyle='--', linewidth=1.5, alpha=0.7)

# 设置背景色
ax.set_facecolor('#FAFAFA')
fig.patch.set_facecolor('white')

plt.tight_layout()

# 创建输出目录并保存

plt.savefig('hour_distributing.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✅ 图像已成功保存")

plt.show()
