
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 加载数据
df = pd.read_csv('ICData.csv', sep=',')
df['交易时间'] = pd.to_datetime(df['交易时间'])
df['hour'] = df['交易时间'].dt.hour
df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])
df = df[df['ride_stops'] != 0]

print("数据加载完成，准备定义函数...")
print(f"数据集形状: {df.shape}")


# ==================== 任务3: 线路站点分析 ====================

def analyze_route_stops(df, route_col='线路号', stops_col='ride_stops'):
    """
    计算各线路乘客的平均搭乘站点数及其标准差。

    Parameters
    ----------
    df : pd.DataFrame  预处理后的数据集
    route_col : str    线路号列名
    stops_col : str    搭乘站点数列名

    Returns
    -------
    pd.DataFrame  包含列：线路号、mean_stops、std_stops，按 mean_stops 降序排列
    """
    # 按线路号分组，计算平均搭乘站点数和标准差
    route_stats = df.groupby(route_col)[stops_col].agg(['mean', 'std', 'count']).reset_index()

    # 重命名列
    route_stats.columns = [route_col, 'mean_stops', 'std_stops', 'count']

    # 按 mean_stops 降序排列
    route_stats = route_stats.sort_values('mean_stops', ascending=False)

    return route_stats


# 1. 调用函数并打印结果（前10行）
print("=" * 60)
print("任务3.1: 调用 analyze_route_stops 函数")
print("=" * 60)

result = analyze_route_stops(df)
print(f"\n各线路平均搭乘站点数统计（共 {len(result)} 条线路）:")
print("\n前10行结果:")
print(result.head(10).to_string(index=False))

print(f"\n统计摘要:")
print(f"  平均站点数最多的线路: {result.iloc[0]['线路号']} (平均 {result.iloc[0]['mean_stops']:.2f} 站)")
print(f"  平均站点数最少的线路: {result.iloc[-1]['线路号']} (平均 {result.iloc[-1]['mean_stops']:.2f} 站)")
print(f"  所有线路平均站点数的中位数: {result['mean_stops'].median():.2f} 站")


# 2. 使用 seaborn 绘制水平条形图（取均值最高的前15条线路）
print("\n" + "=" * 60)
print("任务3.2: seaborn 水平条形图可视化")
print("=" * 60)

# 取均值最高的前15条线路
top15 = result.head(15).copy()

# 将线路号转为字符串（避免被当作数值处理）
top15['线路号'] = top15['线路号'].astype(str)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形
fig, ax = plt.subplots(figsize=(12, 10), dpi=150)

# 使用 seaborn 水平条形图
# 注意：seaborn的barplot中，x是数值，y是分类变量（水平条形图）
sns.barplot(
    data=top15,
    x='mean_stops',
    y='线路号',
    palette='Blues_d',
    errorbar='sd',      # 显示标准差
    capsize=0.3,
    orient='h',
    ax=ax
)

# 设置标题和轴标签
ax.set_title('各线路平均搭乘站点数 TOP15\n（误差棒表示标准差）',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('平均搭乘站点数 (站)', fontsize=14, fontweight='bold')
ax.set_ylabel('线路号', fontsize=14, fontweight='bold')

# X轴从0起始
ax.set_xlim(0, max(top15['mean_stops']) * 1.2)

# 添加数值标签
for i, (idx, row) in enumerate(top15.iterrows()):
    ax.text(row['mean_stops'] + 0.3, i, f"{row['mean_stops']:.2f}",
            va='center', fontsize=10, fontweight='bold')

# 添加网格线
ax.grid(axis='x', linestyle='--', alpha=0.5)

# 调整布局
plt.tight_layout()

# 保存图像
plt.savefig('route_stops.png', dpi=150, bbox_inches='tight', facecolor='white')
print(f"\n✅ 图像已保存")

plt.show()

print(f"\n图表信息:")
print(f"  - 展示线路数: {len(top15)}")
print(f"  - 平均站点数范围: {top15['mean_stops'].min():.2f} ~ {top15['mean_stops'].max():.2f} 站")
print(f"  - 配色方案: Blues_d")
print(f"  - 误差棒: 标准差 (capsize=0.3)")
