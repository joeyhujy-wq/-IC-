import pandas as pd
import os

# 重新加载数据
df = pd.read_csv('ICData.csv', sep=',')

print("=" * 70)
print("任务5: 线路驾驶员信息批量导出")
print("=" * 70)

# 1. 筛选线路号在1101至1120之间的记录
print("\n步骤1: 筛选线路号 1101-1120 的记录")
route_mask = (df['线路号'] >= 1101) & (df['线路号'] <= 1120)
df_filtered = df[route_mask].copy()

unique_routes = sorted(df_filtered['线路号'].unique())
print(f"筛选结果: 共 {len(df_filtered)} 条记录，涉及 {len(unique_routes)} 条线路")
print(f"线路列表: {unique_routes}")

# 2. 创建输出文件夹
print("\n步骤2: 创建输出文件夹")
output_folder = '线路驾驶员信息'
os.makedirs(output_folder, exist_ok=True)
print(f"输出文件夹: {output_folder}")

# 3. 为每条线路生成文件
print("\n步骤3: 生成线路驾驶员信息文件")
print("-" * 50)

generated_files = []

for route in unique_routes:
    # 筛选该线路的记录
    route_data = df_filtered[df_filtered['线路号'] == route]

    # 获取车辆编号 → 驾驶员编号的对应关系（去重）
    vehicle_driver_pairs = route_data[['车辆编号', '驾驶员编号']].drop_duplicates()
    vehicle_driver_pairs = vehicle_driver_pairs.sort_values('车辆编号')

    # 生成文件路径
    file_path = os.path.join(output_folder, f"{route}.txt")

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"线路号: {route}\n")
        f.write("车辆编号\t驾驶员编号\n")
        for _, row in vehicle_driver_pairs.iterrows():
            f.write(f"{row['车辆编号']}\t\t{row['驾驶员编号']}\n")

    generated_files.append(file_path)
    print(f"✓ 线路 {route}: {len(vehicle_driver_pairs)} 条车辆-驾驶员对应关系 -> {route}.txt")

print("-" * 50)


# 4. 打印20个文件的生成路径
print("\n步骤4: 文件生成路径确认")
print("=" * 70)
print(f"\n共生成 {len(generated_files)} 个文件:")
print("-" * 70)

for i, file_path in enumerate(generated_files, 1):
    route = os.path.basename(file_path).replace('.txt', '')
    file_size = os.path.getsize(file_path)
    print(f"{i:2d}. {file_path} ({file_size} bytes)")

print("-" * 70)
print(f"✅ 全部 {len(generated_files)} 个文件输出成功！")

