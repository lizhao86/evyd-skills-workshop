# 统计分析与计算框架

本文件定义 Phase 2 统计分析的具体计算规范。Claude 在分析时参考本文件选择合适的方法。

---

## 1. 数据 Profiling（必做）

每次分析的第一步，自动执行：

```python
import pandas as pd
import numpy as np

df = pd.read_excel("data.xlsx")  # 或 pd.read_csv()

# 基本结构
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Dtypes:\n{df.dtypes}")

# 缺失值
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(1)
print(f"Missing:\n{missing_pct[missing_pct > 0]}")

# 数值列摘要
print(df.describe())

# 重复行
dupes = df.duplicated().sum()
print(f"Duplicate rows: {dupes}")

# 日期范围（如有日期列）
date_cols = df.select_dtypes(include=['datetime64']).columns
for col in date_cols:
    print(f"{col}: {df[col].min()} to {df[col].max()}")
```

### 质检判定规则

| 问题 | 阈值 | 处理 |
|---|---|---|
| 缺失率 | > 30% | 警告，不用该列做核心结论 |
| 缺失率 | 5-30% | 标注，说明处理方式（删除/填充/保留） |
| 重复行 | > 0 | 报告，确认是否去重 |
| 异常值 | \|Z-score\| > 3 | 标记，判断是真实极端值还是数据错误 |
| 样本量 | < 30 | 统计检验标记 `[样本不足，仅供参考]` |

---

## 2. 对比检验

### 2a. 两组比率对比（转化率、留存率等）

场景：本月转化率 vs 上月转化率

```python
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

# 数据
successes = np.array([x1, x2])  # 两期的成功数
trials = np.array([n1, n2])      # 两期的总数

# Z 检验
z_stat, p_value = proportions_ztest(successes, trials)

# 置信区间
ci_low, ci_high = proportion_confint(x1, n1, alpha=0.05, method='wilson')

print(f"p-value: {p_value:.4f}")
print(f"{'显著' if p_value < 0.05 else '不显著'}")
print(f"95% CI: [{ci_low:.3f}, {ci_high:.3f}]")
```

### 2b. 两组均值对比（ARPU、时长等）

场景：A 组 vs B 组的 ARPU

```python
from scipy import stats

t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)

# 效应量 (Cohen's d)
pooled_std = np.sqrt((group_a.std()**2 + group_b.std()**2) / 2)
cohens_d = (group_a.mean() - group_b.mean()) / pooled_std

print(f"p-value: {p_value:.4f}, Cohen's d: {cohens_d:.2f}")
```

效应量解读：
- |d| < 0.2：微小差异
- 0.2 <= |d| < 0.5：小差异
- 0.5 <= |d| < 0.8：中等差异
- |d| >= 0.8：大差异

### 2c. 卡方检验（分类变量关联）

场景：不同渠道的付费率是否有差异

```python
from scipy.stats import chi2_contingency

# 列联表
contingency = pd.crosstab(df['channel'], df['is_paid'])
chi2, p_value, dof, expected = chi2_contingency(contingency)

print(f"Chi2: {chi2:.2f}, p-value: {p_value:.4f}, df: {dof}")
```

### 结果报告规范

所有检验结果必须同时报告：
1. **检验统计量**和 **p-value**
2. **置信区间**（CI）
3. **结论标记**：`[显著]` 或 `[不显著]`
4. **业务含义**：用日常语言解释

示例：
```
问诊转化率从 12.0% 降至 10.2%（差异 -1.8pp，p=0.02 [显著]，95% CI [-3.2pp, -0.4pp]）。
本月转化率确实下降了，真实降幅在 0.4pp 到 3.2pp 之间。
```

---

## 3. 驱动因素拆解

### 3a. 维度拆解（按贡献度排序）

```python
# 两期数据对比
current = df_current.groupby('dimension')['metric'].sum()
previous = df_previous.groupby('dimension')['metric'].sum()

# 各维度变化量
delta = current - previous
total_delta = delta.sum()

# 贡献度
contribution = (delta / total_delta * 100).round(1)
contribution.sort_values(ascending=True if total_delta < 0 else False)
```

输出格式：
```
总体变化: -1,850 (-15.0%)
├── 微信渠道:  -1,443  (贡献 78.0%)
├── 直接访问:    -222  (贡献 12.0%)
├── App Store:   -148  (贡献 8.0%)
└── 其他渠道:     -37  (贡献 2.0%)
```

### 3b. 漏斗分析

```python
# 漏斗数据结构
funnel = pd.DataFrame({
    'step': ['访问', '搜索', '列表', '详情', '下单', '支付'],
    'current': [280000, 142000, 98000, 67000, 23000, 19500],
    'previous': [265000, 128000, 84000, 58000, 18500, 15200]
})

# 转化率
funnel['cvr_current'] = funnel['current'] / funnel['current'].shift(1)
funnel['cvr_previous'] = funnel['previous'] / funnel['previous'].shift(1)
funnel['cvr_delta'] = funnel['cvr_current'] - funnel['cvr_previous']

# 绝对流失量
funnel['loss_current'] = funnel['current'].shift(1) - funnel['current']
```

### 3c. Cohort 留存矩阵

```python
# 构建留存矩阵
def build_retention(df, user_col, date_col, freq='M'):
    df['cohort'] = df.groupby(user_col)[date_col].transform('min').dt.to_period(freq)
    df['period'] = df[date_col].dt.to_period(freq)
    df['period_number'] = (df['period'] - df['cohort']).apply(lambda x: x.n)

    cohort_size = df.groupby('cohort')[user_col].nunique()
    retention = df.groupby(['cohort', 'period_number'])[user_col].nunique().unstack()
    retention = retention.divide(cohort_size, axis=0)
    return retention

retention_matrix = build_retention(df, 'user_id', 'event_date', freq='M')
```

输出为留存热力图（行=cohort 批次，列=第 N 月，值=留存率）。

### 3d. 量价拆解

```python
# 收入 = 量 × 价
q_current, q_previous = current_orders, previous_orders
p_current, p_previous = current_aov, previous_aov

delta_revenue = q_current * p_current - q_previous * p_previous
volume_effect = (q_current - q_previous) * p_previous
price_effect = q_previous * (p_current - p_previous)
mix_effect = (q_current - q_previous) * (p_current - p_previous)

print(f"收入变化: {delta_revenue:,.0f}")
print(f"├── 量变化贡献: {volume_effect:,.0f} ({volume_effect/delta_revenue*100:.1f}%)")
print(f"├── 价变化贡献: {price_effect:,.0f} ({price_effect/delta_revenue*100:.1f}%)")
print(f"└── 交叉项: {mix_effect:,.0f} ({mix_effect/delta_revenue*100:.1f}%)")
```

---

## 4. 趋势与异常检测

### 4a. 移动平均

```python
df['ma7'] = df['metric'].rolling(window=7, min_periods=1).mean()
df['ma30'] = df['metric'].rolling(window=30, min_periods=1).mean()
```

### 4b. Z-score 异常检测

```python
mean = df['metric'].mean()
std = df['metric'].std()
df['zscore'] = (df['metric'] - mean) / std
anomalies = df[df['zscore'].abs() > 2]

print(f"异常点: {len(anomalies)} 个")
for _, row in anomalies.iterrows():
    direction = '高' if row['zscore'] > 0 else '低'
    print(f"  {row['date']}: {row['metric']} (偏{direction} {abs(row['zscore']):.1f} 个标准差)")
```

### 4c. 环比变化率异常

```python
df['pct_change'] = df['metric'].pct_change()
threshold = df['pct_change'].std() * 2
anomalies = df[df['pct_change'].abs() > threshold]
```

---

## 5. AB 测试分析

### 前置检查

1. **样本量充足性**：
```python
from statsmodels.stats.power import NormalIndPower

power_analysis = NormalIndPower()
n_required = power_analysis.solve_power(
    effect_size=0.05,   # 最小可检测效应（MDE）
    alpha=0.05,
    power=0.8,
    alternative='two-sided'
)
print(f"每组最少需要 {int(n_required)} 样本")
```

2. **SRM 检查**（Sample Ratio Mismatch）：
```python
from scipy.stats import binomtest
result = binomtest(n_control, n_control + n_variant, p=expected_ratio)
if result.pvalue < 0.01:
    print("WARNING: SRM detected, randomization may be broken")
```

3. **持续时间**：至少覆盖 1-2 个完整业务周期（通常 7-14 天）

### 结果分析

```python
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

# 转化率对比
successes = np.array([control_conversions, variant_conversions])
trials = np.array([n_control, n_variant])

z_stat, p_value = proportions_ztest(successes, trials)

# 相对提升
control_rate = control_conversions / n_control
variant_rate = variant_conversions / n_variant
lift = (variant_rate - control_rate) / control_rate * 100

print(f"Control: {control_rate:.3%}")
print(f"Variant: {variant_rate:.3%}")
print(f"Lift: {lift:+.1f}%")
print(f"p-value: {p_value:.4f}")
```

### 决策矩阵

| 结果 | p-value | 建议 |
|---|---|---|
| 显著正向提升，无 guardrail 问题 | < 0.05 | 全量上线 |
| 显著正向提升，guardrail 有降 | < 0.05 | 调查权衡后决定 |
| 正向趋势但不显著 | >= 0.05 | 延长测试或扩大样本 |
| 无差异 | >= 0.05 | 停止测试，无效果 |
| 显著负向 | < 0.05 | 不上线，回滚到对照组 |

---

## 6. 可视化规范

### 中文字体配置

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'SimHei', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False
```

### 图表保存

所有图表保存到 `/tmp/evyd-analysis/`：

```python
import os
os.makedirs('/tmp/evyd-analysis', exist_ok=True)
fig.savefig('/tmp/evyd-analysis/chart_name.png', dpi=150, bbox_inches='tight')
```

### 常用图表类型选择

| 数据类型 | 推荐图表 | PPT 对应（全 freeform） |
|---|---|---|
| 时间趋势 | 折线图 | freeform: rect 比例条 + text 标注 |
| 维度对比 | 横向条形图 | freeform: rect 横向条形（宽度比例 = 数值比例）+ text |
| 构成/占比 | 饼图/环形图 | freeform: rect 堆叠条 + text 百分比标注 |
| 留存矩阵 | 热力图 | freeform: 导出 PNG 后用 image element |
| 漏斗 | 横向条形图（降序） | freeform: rect 宽度递减 + text 转化率 |
| 分布 | 直方图/箱线图 | freeform: 导出 PNG 后用 image element |
| 核心数字 | 大数字卡片 | freeform: rect 卡片 + text（大号数字 sz ≥ 44 + 标签 + 说明）|

> **注意：** 所有 PPT 幻灯片统一使用 `freeform` 类型。不使用 `stat_highlight`、`chart`、`ending` 等结构化类型。正文字号 ≥ 18，来源标注 sz 12 独立置于页面底部。

### 颜色规范

与 `evyd-ppt-generator` 的 `evyd_blue` 风格对齐：
- 主色：`#2CD5C3`（teal）
- 辅色：`#0076B3`（blue）
- 强调：`#E87722`（orange，用于异常/警告）
- 背景：`#172E41`（navy）

```python
EVYD_COLORS = {
    'teal': '#2CD5C3',
    'blue': '#0076B3',
    'orange': '#E87722',
    'navy': '#172E41',
    'light': '#EFF7FD',
    'gray': '#446688',
}
```
