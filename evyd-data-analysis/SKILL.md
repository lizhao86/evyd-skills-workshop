---
name: evyd-data-analysis
description: >
  Use when the user provides an Excel/CSV dataset and needs structured data analysis:
  descriptive facts, driver decomposition, statistical insights, and actionable product/operations
  recommendations for management reporting. Trigger on 数据分析, 分析一下, data analysis,
  帮我看看数据, 指标诊断, metric diagnosis, 数据洞察, data insight.
  Also use when user says 生成分析PPT, 出报告, or wants to chain output into evyd-ppt-generator.
---

# EVYD Data Analysis

从 Excel/CSV 数据到管理层可用的分析报告：事实描述 → 洞察拆解 → 行动建议。

## 核心原则

先定义问题，再统一口径，再看数据质量，再做诊断，最后给动作。

- **先问题后动作**：先写清决策问题、对象、时间范围、比较基准
- **先口径后结论**：任何同比/环比/转化率/ARPU，都先定义分子、分母、时间窗
- **先验数后解释**：先检查样本量、缺失值、重复值、口径漂移，再做业务判断
- **先拆结构后下结论**：总体变化必须拆到渠道/地区/客群/产品/时间等维度
- **先区分事实与推断**：标记 `[已知]` `[推断]` `[假设]` `[风险]`
- **结论必须能落动作**：每条建议回答"做什么、谁去做、看什么指标、观察多久"

## 工作流程

### Phase 0 — 确认场景

用户丢来数据后，先问清楚：

1. **决策问题**：这份数据要回答什么问题？（例："3 月 DAU 为什么跌了"）
2. **比较基准**：对比什么？（环比上月 / 同比去年 / 对比目标值）
3. **输出对象**：给谁看？（默认管理层，简洁结论优先）
4. **是否需要 PPT**：是否需要联动 `evyd-ppt-generator` 生成演示文稿

如果用户直接说"帮我分析一下"且意图清晰，可跳过追问，默认：环比上期、管理层视角。

### Phase 1 — 数据摄入与逐 Sheet 澄清

**核心原则：先读懂数据，再分析数据。不理解的不分析。**

#### Step 1.1 — 文件级扫描

读取用户提供的 Excel/CSV 文件，先做结构扫描（不做任何分析）：

```python
import pandas as pd

xls = pd.ExcelFile("data.xlsx")
print(f"文件: data.xlsx")
print(f"Sheet 数: {len(xls.sheet_names)}")
for s in xls.sheet_names:
    df = pd.read_excel(xls, s)
    print(f"  Sheet '{s}': {df.shape[0]} 行 × {df.shape[1]} 列")
    print(f"    列名: {list(df.columns)}")
```

如果有多个文件，逐个扫描。

#### Step 1.2 — 逐 Sheet 解读与澄清

**对每个 Sheet，先输出解读摘要，让用户确认。格式：**

```
📋 Sheet "{name}" 解读

我的理解：
- 这张表记录的是：{一句话描述}
- 维度列：{列名} = {含义}
- 指标列：{列名} = {含义}（口径：{分子/分母/时间窗}）
- 数据粒度：{每行代表什么}
- 时间范围：{如有}
- 关键注释：{Excel 中的备注/注释文字}

疑问（需要你确认）：
- {列名} 的含义不确定，可能是 A 也可能是 B？
- {数字} 出现在表头/批注中，它代表什么？
- 这张表和 Sheet "{other}" 的关系是？
```

**澄清规则：**
- 遇到 Excel 表头中嵌入的计算公式（如 "169317/215595*100%=78.53%"），原样呈现，说明自己的理解，问用户对不对
- 遇到不确定的缩写或业务术语（如 HSD、RA、OVA），必须问
- 遇到同一指标在不同 Sheet 中数值不同，标记差异并问
- 遇到 Sheet 中大量空行/合并单元格导致结构不清，说明解析困难并展示原始读取结果
- **不要猜测后直接分析，必须等用户确认**

#### Step 1.3 — 用户确认后，建立数据字典

用户确认后，输出完整的数据字典作为后续分析的唯一 reference：

```
📖 数据字典（已确认）

来源文件: {filename}
总 Sheet 数: {N}

| Sheet | 描述 | 维度 | 指标 | 行数 | 备注 |
|---|---|---|---|---|---|
| Sheet 1 | 各模块新老用户分布 | module, user_type, times | user_cnt | 83 | New=2025.04-2026.04注册 |
| Sheet 2 | HSD 总用户与频次 | times | total_user | 5 | 平台总用户=215,595 |
| ... | ... | ... | ... | ... | ... |
```

**所有后续分析中引用数据时，必须标注来源 Sheet。**

#### Step 1.4 — 数据质检

在数据字典确认后，对每个 Sheet 执行质检：

```python
# 基本质检
missing = df.isnull().sum()
print(f"缺失值:\n{missing[missing > 0]}")
print(f"重复行: {df.duplicated().sum()}")
print(df.describe())
```

输出质检摘要：

```
🔍 数据质检

- Sheet 1: 83 行，缺失值 0，数据完整
- Sheet 2: 8 行，其中 3 行为空/注释行，有效数据 5 行
- Sheet 4: 表头嵌入汇总数据，数据区从第 14 行开始
- 整体可信度：[可信 / 需注意 {issue}]
```

**质检红线**：
- 缺失率 > 30% 的列 → 警告用户，不用该列做核心结论
- 明显的口径变更（如某日数据突变但非业务原因）→ 标记 `[风险]`
- 样本量 < 30 → 统计检验结论标记 `[样本不足，仅供参考]`
- 同一指标在不同 Sheet 中数值不一致 → 停下来问用户以哪个为准

### Phase 2 — 统计分析

根据数据类型和用户问题，自动选择分析方法：

#### 2a. 描述性统计（必做）

- 核心指标的均值、中位数、标准差、分位数
- 时间趋势（如有日期列）：逐期变化、环比/同比
- 分布特征：是否偏态、是否有聚集

#### 2b. 对比检验（当涉及"是否真的变了"）

```python
from scipy import stats

# 两组比率对比（如转化率变化）
z_stat, p_value = proportions_ztest([x1, x2], [n1, n2])

# 两组均值对比（如 ARPU 变化）
t_stat, p_value = stats.ttest_ind(group_a, group_b)

# 置信区间
import statsmodels.api as sm
ci = sm.stats.proportion_confint(successes, trials, alpha=0.05)
```

结果标记规则：
- `p < 0.05` → `[显著]` 可以当真
- `p >= 0.05` → `[不显著]` 可能只是波动
- 同时报告置信区间 `[CI: x% ~ y%]`

#### 2c. 驱动因素拆解（核心分析）

总体变化必须拆到子维度，按贡献度排序：

```python
# 示例：DAU 下降的渠道拆解
contribution = df.groupby('channel')['dau'].agg(['sum'])
contribution['pct'] = contribution['sum'] / contribution['sum'].sum() * 100
contribution['delta'] = ...  # 对比基准期
contribution.sort_values('delta', ascending=True)
```

常用拆解维度：
- 渠道 / 地区 / 客群 / 产品线 / 新老用户
- 漏斗各环节（访问→注册→激活→下单→支付）
- Cohort 批次（按注册月/首购月分组）

#### 2d. 趋势与异常检测（如有时间序列）

```python
# 移动平均识别趋势
df['ma7'] = df['metric'].rolling(7).mean()

# Z-score 识别异常点
df['zscore'] = (df['metric'] - df['metric'].mean()) / df['metric'].std()
anomalies = df[df['zscore'].abs() > 2]
```

#### 2e. 可视化（按需生成）

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 趋势图
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df['date'], df['metric'], marker='o')
ax.set_title('DAU 趋势')
fig.savefig('/tmp/trend.png', dpi=150, bbox_inches='tight')

# 留存热力图
import seaborn as sns
sns.heatmap(retention_matrix, annot=True, fmt='.0%', cmap='YlOrRd_r')
```

图表保存到 `/tmp/evyd-analysis/` 供报告引用或 PPT 使用。

### Phase 3 — 输出报告

**三层结构，严格分离，顺序固定。每条 fact 必须标注数据来源。**

---

```markdown
# {分析主题} — 数据分析报告

> 决策问题：{一句话}
> 数据范围：{时间/来源/口径}
> 分析日期：{YYYY-MM-DD}

---

## 数据字典（简版）

| 来源 | Sheet | 描述 | 关键指标 |
|---|---|---|---|
| data.xlsx | Sheet 1 | 各模块新老用户分布 | user_cnt by module × user_type × times |
| data.xlsx | Sheet 2 | HSD 用户频次分布 | total_user by times |
| ... | ... | ... | ... |

---

## Data Facts — 发生了什么

只写观察到的事实，不混入主观判断。
**每条必须标注 [来源: 文件名/Sheet名/列名或计算公式]。**

- [已知] DAU 从 12,340 降至 10,490，环比 -15.0%
  [来源: data.xlsx / Sheet "daily" / dau 列，sum(3月) vs sum(2月)]
- [已知] 微信渠道 DAU 降幅 22%，贡献总跌幅 78%
  [来源: data.xlsx / Sheet "daily" / channel="wechat"，(12340-10490) 中 wechat delta 占比]
- [已知] 问诊转化率 11.2% → 10.8%（p=0.31，不显著）
  [来源: data.xlsx / Sheet "funnel" / consult_starts / page_views]

**来源标注规则：**
- 直接读取的数字 → 标注 Sheet + 列 + 行范围
- 计算得出的数字 → 标注计算公式 + 输入数据来源
- Excel 表头/批注中嵌入的数字 → 标注 "Sheet X 表头注释"
- 交叉计算（跨 Sheet / 跨文件）→ 分别标注两个来源

## Insights — 为什么 / 意味着什么

驱动因素按影响大小排序。标记 [已知] / [推断] / [假设]。

1. [已知] 微信渠道贡献了总跌幅的 78%
   [来源: 同 Facts 第 2 条的渠道拆解]
2. [推断] 3 月 15 日微信入口改版可能是触发点
   [依据: 时间吻合，但无 AB 数据直接证明]
3. [假设] 转化率微降可能是流量质量下降的连带效应
   [需验证: 需按渠道拆转化率，对比微信 vs 非微信]

## Actions — 该做什么

1-3 条，禁止空话。每条包含 6 个字段：

| 字段 | 说明 |
|---|---|
| **行动** | 具体做什么（一句话） |
| **负责人** | 哪个角色/团队 |
| **分析方法** | 具体怎么验证——查什么数据、对比什么时间段、看什么指标、在哪个平台取数 |
| **判定标准** | 什么结果算"确认"，什么算"排除" |
| **观察期** | 多长时间 |
| **风险** | 可能的干扰因素 |

示例：

**1. 排查微信入口改版影响**
- 负责人：产品/增长
- 分析方法：从埋点平台导出 3/1-3/31 的微信渠道 DAU 日数据 + 入口页 Page UV，按改版日期（3/15）切分前后两段，对比入口页 UV 和 DAU 的变化幅度。同时拉非微信渠道同时段数据作为对照组
- 判定标准：若微信入口页 UV 在 3/15 后下降 >10% 且非微信渠道无同等跌幅 → 确认改版影响；若两组同步下降 → 排除改版，需扩大排查
- 观察期：7 天（拿到数据后）
- 风险：若 3/15 同时有其他变更（推送策略、投放调整），需逐一排除

**2. （暂不行动）转化率变化不显著，继续监控**
- 负责人：BI
- 分析方法：每周一从 BI 报表导出转化率（口径：consult_starts / detail_page_uv），按周汇总，观察是否连续 3 周下降趋势
- 判定标准：连续 3 周环比下降且累计降幅 > 2pp → 升级为正式分析课题
- 观察期：持续
- 风险：无

## 信息缺口

- [ ] {缺什么数据} — 谁能提供 — 拿到后可以验证什么
- [ ] {缺什么上下文} — 谁能确认 — 影响哪条 Insight 的判定
```

---

### Phase 4（可选）— 联动 PPT 生成

当用户要求生成 PPT 时，将分析结果转为 `evyd-ppt-generator` 的 `content.json`。

#### 幻灯片类型：全部使用 freeform

**所有幻灯片默认使用 `freeform` 类型。** 不使用 `stat_highlight`、`chart`、`two_column_steps`、`ending` 等结构化类型 — 它们的排版自由度不够，容易在复杂数据页上出现溢出或对齐问题。

用 freeform 的 element 组合实现所有效果：

| 报告内容 | freeform 实现方式 | 说明 |
|---|---|---|
| 封面（标题 + 决策问题） | gradient 背景 + text 元素 | 大标题 sz ≥ 40，副标题 sz ≥ 20 |
| 核心数字卡片 | rect 卡片 + text（大数字 + 标签 + 说明） | 每个数字一个 rect，横排 2-4 个 |
| 趋势 / 对比图 | rect 比例条 + text 标注 | 用 rect 宽度比例表达数值对比 |
| 驱动因素拆解 | rect 横向条形 + text | 按贡献度排序，颜色区分 |
| Insights 摘要 | text 列表 + rect 分隔 | 2-3 条核心洞察 |
| Actions 行动计划 | rect 卡片 + text | 每条 Action 一个卡片 |
| 信息缺口 | text 列表 | ending 前一页 |
| 尾页 | gradient 背景 + text | 感谢 + 联系方式 |

#### PPT 排版铁律

1. **字号下限**：正文/卡片文字 sz ≥ 18，标题 sz ≥ 36，面包屑/section sz ≥ 12。`validate_and_fix()` 最多向下收缩 4pt，低于 18pt 的正文会导致不可读。
2. **数据来源必须独立成行**：每个包含数据的页面，底部必须有一个独立的 text 元素作为来源标注（sz 12，color `text_dim`，y 位置 ≥ 9.5）。**禁止**将来源信息嵌入卡片 body 或正文段落中 — 嵌入式来源在视觉上不可识别，审阅者无法快速定位数据出处。
3. **来源标注格式**：`来源: {filename} / Sheet {name} / {column 或 calculation}`，跨 Sheet 计算需分别列出两个来源。
4. **画布坐标**：20″ × 11.25″（16:9 2× 标准），所有元素的 x+w ≤ 20, y+h ≤ 11.25。

#### PPT 联动流程

1. 基于分析结果生成 `content.json`，使用 Narrative Template E (Pyramid/Executive)
2. **所有 slides 的 type 设为 `freeform`**，不使用任何结构化类型
3. 风格默认 `evyd_blue`（管理层汇报），用户可指定
4. 调用 PPT 生成器：
   ```bash
   cd "/Users/Li.ZHAO/我的代码/evyd-skills-workshop/evyd-ppt-generator"
   python3 gen_pptx.py /tmp/evyd-analysis/content.json --style evyd_blue \
     --output "/Users/Li.ZHAO/Desktop/数据分析报告.pptx"
   ```
5. 执行 PPT QA 流程（参见 evyd-ppt-generator Phase 5）
6. **QA 必查项**：逐页检查是否有独立的来源标注行，字号是否 ≥ 18（正文）/ ≥ 12（来源）

#### content.json 生成示例（全 freeform）

```json
{
  "meta": { "style": "evyd_blue", "output": "/Users/Li.ZHAO/Desktop/数据分析报告.pptx" },
  "slides": [
    {
      "type": "freeform", "section": "", "elements": [
        { "kind": "gradient", "x": 0, "y": 0, "w": 20, "h": 11.25, "colors": ["navy", "0D3B5C"], "angle": 135 },
        { "kind": "text", "x": 1.5, "y": 3.0, "w": 17, "h": 2.0, "text": "3 月 DAU 下降分析", "sz": 44, "bold": true, "color": "white" },
        { "kind": "text", "x": 1.5, "y": 5.5, "w": 17, "h": 1.5, "text": "决策问题：DAU 环比下降 15%，定位原因并给出恢复方案", "sz": 20, "color": "text_dim" }
      ]
    },
    {
      "type": "freeform", "section": "01 — Key Facts", "elements": [
        { "kind": "rect", "x": 0, "y": 0, "w": 20, "h": 11.25, "fill": "card" },
        { "kind": "text", "x": 1.0, "y": 0.3, "w": 18, "h": 0.6, "text": "01 — Key Facts", "sz": 12, "color": "text_dim" },
        { "kind": "text", "x": 1.0, "y": 1.0, "w": 18, "h": 1.0, "text": "核心指标", "sz": 36, "bold": true, "color": "navy" },
        { "kind": "rect", "x": 1.0, "y": 2.5, "w": 5.5, "h": 5.5, "fill": "white", "radius": 0.2 },
        { "kind": "text", "x": 1.5, "y": 3.0, "w": 4.5, "h": 1.5, "text": "-15%", "sz": 48, "bold": true, "color": "accent" },
        { "kind": "text", "x": 1.5, "y": 4.8, "w": 4.5, "h": 0.6, "text": "DAU 环比", "sz": 20, "bold": true },
        { "kind": "text", "x": 1.5, "y": 5.6, "w": 4.5, "h": 1.5, "text": "10,490 vs 12,340", "sz": 18, "color": "text_dim" },
        { "kind": "rect", "x": 7.25, "y": 2.5, "w": 5.5, "h": 5.5, "fill": "white", "radius": 0.2 },
        { "kind": "text", "x": 7.75, "y": 3.0, "w": 4.5, "h": 1.5, "text": "78%", "sz": 48, "bold": true, "color": "accent" },
        { "kind": "text", "x": 7.75, "y": 4.8, "w": 4.5, "h": 0.6, "text": "微信贡献", "sz": 20, "bold": true },
        { "kind": "text", "x": 7.75, "y": 5.6, "w": 4.5, "h": 1.5, "text": "跌幅主因", "sz": 18, "color": "text_dim" },
        { "kind": "rect", "x": 13.5, "y": 2.5, "w": 5.5, "h": 5.5, "fill": "white", "radius": 0.2 },
        { "kind": "text", "x": 14.0, "y": 3.0, "w": 4.5, "h": 1.5, "text": "p=0.008", "sz": 48, "bold": true, "color": "accent" },
        { "kind": "text", "x": 14.0, "y": 4.8, "w": 4.5, "h": 0.6, "text": "统计显著", "sz": 20, "bold": true },
        { "kind": "text", "x": 14.0, "y": 5.6, "w": 4.5, "h": 1.5, "text": "非随机波动", "sz": 18, "color": "text_dim" },
        { "kind": "text", "x": 1.0, "y": 10.0, "w": 18, "h": 0.5, "text": "来源: daily_metrics.xlsx / Sheet \"DAU\" / dau 列 avg(3月) vs avg(2月), channel 拆解", "sz": 12, "color": "text_dim" }
      ]
    },
    {
      "type": "freeform", "section": "01 — Key Facts", "elements": [
        { "kind": "rect", "x": 0, "y": 0, "w": 20, "h": 11.25, "fill": "white" },
        { "kind": "text", "x": 1.0, "y": 0.3, "w": 18, "h": 0.6, "text": "01 — Key Facts", "sz": 12, "color": "text_dim" },
        { "kind": "text", "x": 1.0, "y": 1.0, "w": 18, "h": 1.0, "text": "DAU 日趋势与渠道拆解", "sz": 36, "bold": true },
        { "kind": "rect", "x": 1.0, "y": 2.5, "w": 14, "h": 0.8, "fill": "accent", "radius": 0.1 },
        { "kind": "text", "x": 1.2, "y": 2.55, "w": 5, "h": 0.7, "text": "微信  -22%", "sz": 18, "bold": true, "color": "white" },
        { "kind": "rect", "x": 1.0, "y": 3.5, "w": 3, "h": 0.8, "fill": "navy", "radius": 0.1 },
        { "kind": "text", "x": 1.2, "y": 3.55, "w": 5, "h": 0.7, "text": "直接访问  -8%", "sz": 18, "bold": true, "color": "white" },
        { "kind": "rect", "x": 1.0, "y": 4.5, "w": 2, "h": 0.8, "fill": "text_dim", "radius": 0.1 },
        { "kind": "text", "x": 1.2, "y": 4.55, "w": 5, "h": 0.7, "text": "App Store  -3%", "sz": 18, "color": "white" },
        { "kind": "text", "x": 1.0, "y": 10.0, "w": 18, "h": 0.5, "text": "来源: daily_metrics.xlsx / Sheet \"DAU\" / channel 分组, sum 对比 3月 vs 2月", "sz": 12, "color": "text_dim" }
      ]
    }
  ]
}
```

**注意：** 每个数据页的最后一个 element 必须是独立的来源标注 text，y ≥ 9.5，sz 12，color `text_dim`。

---

## 五大分析框架

根据用户问题，自动选择合适的框架。详见 `references/analysis-frameworks.md`。

| 框架 | 适用场景 | 核心拆法 |
|---|---|---|
| **增长分析** | DAU/MAU/收入增长放缓 | 流量 × 转化 × ARPU × 留存 × 渠道结构 |
| **漏斗分析** | 注册/激活/问诊/支付转化 | 每层转化率 + 流失量 + 最大损失环节 + 分群差异 |
| **留存 & Cohort** | 用户流失/复购/续费 | 不同批次留存曲线 + 获客结构 vs 产品体验 |
| **收入 & 利润** | 经营复盘/ARPU 变化 | 量 × 价 × 折扣 × 产品结构 × 渠道结构 |
| **运营效率** | 客服/交付/人效问题 | 单位产出 × 单位成本 × 周期 × 利用率 |

## 不要这样做

**数据理解阶段：**
- 不要跳过逐 Sheet 解读直接开始分析——用户给的 Excel 往往结构复杂，不确认就分析 = 在错误理解上做推导
- 不要对不理解的缩写、术语、口径自行猜测——必须问
- 不要忽略 Excel 表头/批注中嵌入的公式和注释——这些往往是关键口径定义

**分析阶段：**
- 不要在口径不清时直接给结论
- 不要只看总体均值，不看结构变化
- 不要把相关性直接写成因果
- 不要把一次活动、节假日、政策扰动当作长期趋势

**输出阶段：**
- 不要写没有来源标注的数字——每个数字必须可追溯到具体 Sheet + 列 + 计算方式
- 不要在 Data Facts 里混入主观判断
- 不要在 Insights 里跳过统计检验直接下因果结论
- 不要给"加强运营""提升转化"这种不可执行建议
- 不要给没有具体分析方法/验证方法的 Action——"观察 7 天"不够，要说清看什么指标、从哪取数、对比什么基准
- 不要在没有业务影响量化时排序优先级
- 不要生成超过 3 条 Action（管理层只看最重要的）

**PPT 生成阶段：**
- 不要使用 `stat_highlight`、`chart`、`ending` 等结构化类型——全部用 `freeform`
- 不要将来源标注嵌入正文或卡片 body——必须是页面底部独立 text element
- 不要让正文/卡片文字 sz < 18——投屏时不可读
- 不要忘记在每个数据页添加来源行——缺来源 = 不可审计

## 输出渠道

分析报告按 `../evyd-output-channels/SKILL.md` 中 active channel 的协议输出。

| 渠道 | 输出形式 |
|---|---|
| `local-markdown` | `/tmp/evyd-analysis/{topic}-{date}.md` + 图表 PNG |
| `feishu` | 飞书文档（列表格式，不用 Markdown 表格） |
| `confluence` | 创建分析页面 |
| PPT 联动 | `content.json` → `evyd-ppt-generator` |

## References 索引

| 文件 | 内容 | 何时读取 |
|---|---|---|
| `references/metric-playbook.md` | 常见指标定义与拆解手册 | 统一口径时 |
| `references/examples.md` | 医疗互联网分析案例 | 需要参考输出格式时 |
| `references/analysis-frameworks.md` | 统计方法与计算规范 | Phase 2 选择分析方法时 |

## 快速示例

```
帮我分析一下这个 Excel                    # 通用分析
3 月 DAU 为什么跌了？[附件 data.xlsx]      # 带明确问题
分析完帮我出个 PPT                         # 联动 PPT 生成
这个留存数据帮我做 cohort 分析             # 指定框架
```
