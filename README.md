# -IC-
公交 IC 卡刷卡数据分析
胡家瑜-25306025-第三次人工智能编程作业

1. 任务拆解与 AI 协作策略
对于每个任务，我先让AI读取数据，再一步一步生成代码，并将每一步生成的代码都亲自运行检验一次，直到结果无误为止。

2.核心 Prompt 迭代记录
AI生成的问题主要有：直接用“seaborn.heatmap()”替代了“matplotlib”，柱状图也试图用seaborn绘制；在任务6生成了4个独立子图，而非题目要求的“4行×10列单张热力图”。
我要求AI严格按规范完成任务6：排名统计用pandas，热力图必须用seaborn.heatmap()，且图片是单张4×10矩阵。AI理解了我的意思，得出了改进后的答案。

3.Debug 记录
代码几乎没有运行错误，主要在于中文读取和显示方面，一般加上plt.rcParams['figure.figsize'] = (12, 8)就可以解决。

4.人工代码审查（逐行中文注释）
任务1如果存在缺失值的处理部分：
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
