
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_csv('ICData.csv', sep=',', encoding='utf-8')
print("数据形状:", df.shape)
print("列名:", df.columns.tolist())
print("\n前5行数据:")
print(df.head())


# 任务6：服务绩效排名与热力图

# 1. 排名统计：分别找出服务人次最多的 Top 10 司机、Top 10 线路、Top 10 上车站点 和 Top 10 车辆

print("=" * 60)
print("任务6：服务绩效排名与热力图")
print("=" * 60)

# 只统计刷卡类型=0的记录（上车刷卡）
df_boarding = df[df['刷卡类型'] == 0].copy()
print(f"\n有效刷卡记录数（刷卡类型=0）: {len(df_boarding)}")

# Top 10 司机（以驾驶员编号为维度）
# 每条记录代表一名乘客一次上车，所以直接统计记录数
top10_drivers = df_boarding['驾驶员编号'].value_counts().head(10)
print("\n" + "=" * 40)
print("Top 10 司机（服务人次）")
print("=" * 40)
for i, (driver_id, count) in enumerate(top10_drivers.items(), 1):
    print(f"Top{i}: 司机 {int(driver_id)} - {count} 人次")

# Top 10 线路
top10_routes = df_boarding['线路号'].value_counts().head(10)
print("\n" + "=" * 40)
print("Top 10 线路（服务人次）")
print("=" * 40)
for i, (route_id, count) in enumerate(top10_routes.items(), 1):
    print(f"Top{i}: 线路 {route_id} - {count} 人次")

# Top 10 上车站点
top10_stops = df_boarding['上车站点'].value_counts().head(10)
print("\n" + "=" * 40)
print("Top 10 上车站点（服务人次）")
print("=" * 40)
for i, (stop_id, count) in enumerate(top10_stops.items(), 1):
    print(f"Top{i}: 站点 {int(stop_id)} - {count} 人次")

# Top 10 车辆
top10_vehicles = df_boarding['车辆编号'].value_counts().head(10)
print("\n" + "=" * 40)
print("Top 10 车辆（服务人次）")
print("=" * 40)
for i, (vehicle_id, count) in enumerate(top10_vehicles.items(), 1):
    print(f"Top{i}: 车辆 {vehicle_id} - {count} 人次")


# 2. 热力图可视化（seaborn heatmap）
# 构造一个 4×10 的热力图（行=4个维度，列=各维度的Top10实体）

# 准备数据：提取各维度Top10的服务人次
heatmap_data = np.zeros((4, 10))

# 行0: 司机
heatmap_data[0] = top10_drivers.values
# 行1: 线路
heatmap_data[1] = top10_routes.values
# 行2: 上车站点
heatmap_data[2] = top10_stops.values
# 行3: 车辆
heatmap_data[3] = top10_vehicles.values

# 创建标签
row_labels = ['司机', '线路', '上车站点', '车辆']
col_labels = [f'Top{i+1}' for i in range(10)]

# 创建DataFrame用于热力图
heatmap_df = pd.DataFrame(heatmap_data, index=row_labels, columns=col_labels)

print("热力图数据矩阵:")
print(heatmap_df)
print(f"\n数据形状: {heatmap_df.shape}")


# 绘制热力图
fig, ax = plt.subplots(figsize=(14, 6))

# 使用YlOrRd colormap，annot=True标注数值
sns.heatmap(
    heatmap_df,
    annot=True,           # 在每个格子中标注数值
    fmt='.0f',            # 数值格式化为整数
    cmap='YlOrRd',        # 使用黄-橙-红渐变色
    linewidths=0.5,       # 格子间线宽
    linecolor='white',    # 格子间线颜色
    cbar_kws={'label': '服务人次'},  # 色条标签
    ax=ax
)

# 设置标题和标签
ax.set_title('公交服务绩效排名热力图（Top10）', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('排名', fontsize=12)
ax.set_ylabel('维度', fontsize=12)

# x轴标签旋转0度（水平显示）
ax.set_xticklabels(col_labels, rotation=0, ha='center')
ax.set_yticklabels(row_labels, rotation=0, va='center')

# 添加副标题说明
fig.text(0.5, 0.02, '数据来源：IC卡刷卡数据 | 统计维度：司机、线路、上车站点、车辆',
         ha='center', fontsize=10, style='italic', color='gray')

plt.tight_layout()
plt.subplots_adjust(bottom=0.12)

# 保存图像
output_path = 'performance_heatmap.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"✅ 图像已保存")

plt.show()
