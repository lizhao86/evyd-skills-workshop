#!/usr/bin/env python3
"""
Ned 每周工作报告生成器
从 Obsidian 读取本周日报、工作思考和会议纪要，生成周报并保存
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# 获取 Vault 路径（支持环境变量或默认路径）
def get_vault_path():
    """获取 Obsidian Vault 路径"""
    return os.environ.get("OBSIDIAN_VAULT_PATH", 
                          os.path.expanduser("~/我赵立的仓库"))

VAULT_PATH = get_vault_path()
DAILY_REPORTS_DIR = os.path.join(VAULT_PATH, "24-Work-周报汇总")
THOUGHTS_DIR = os.path.join(VAULT_PATH, "22-Work-工作思考 🤔")
MEETING_NOTES_DIR = os.path.join(VAULT_PATH, "21-Work-会议纪要 💼")
OUTPUT_DIR = DAILY_REPORTS_DIR

# 业务板块关键词映射
CATEGORY_KEYWORDS = {
    "产品开发": ["routines", "health index", "hi", "功能", "迭代", "开发", "技术"],
    "客户项目": ["nuhs", "sengkang", "ripas", "client", "proposal", "客户", "合作", "医院"],
    "数据分析": ["bi", "uag", "dau", "数据", "分析", "metrics", "dashboard", "埋点"],
    "产品设计": ["oyen", "challenge", "21天", "习惯", "ui", "ux", "设计", "视觉", "交互"],
    "团队管理": ["团队", "管理", "人员", "招聘", "流程", "协作", "会议", "对齐"],
    "战略规划": ["战略", "roadmap", "规划", "方向", "愿景", "优先级", "资源"]
}

def get_week_range(date=None):
    """获取本周的日期范围（周一到周五/今天）"""
    if date is None:
        date = datetime.now()
    
    # 找到本周一
    monday = date - timedelta(days=date.weekday())
    
    # 找到本周五（或今天，如果今天还没到周五）
    friday = monday + timedelta(days=4)
    if date < friday:
        end_date = date
    else:
        end_date = friday
    
    return monday, end_date

def format_date(date):
    """格式化日期为 YYYY-MM-DD"""
    return date.strftime("%Y-%m-%d")

def parse_date_from_filename(filename):
    """从文件名中提取日期"""
    # 匹配 YYYY-MM-DD 格式
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return None

def is_date_in_range(date_str, start_date, end_date):
    """检查日期是否在范围内"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return start_date <= date <= end_date
    except:
        return False

def find_daily_reports(start_date, end_date):
    """查找本周的日报文件"""
    reports = []
    if not os.path.exists(DAILY_REPORTS_DIR):
        return reports
    
    for filename in os.listdir(DAILY_REPORTS_DIR):
        if filename.endswith(".md") and "EVYD 日报" in filename:
            date_str = parse_date_from_filename(filename)
            if date_str and is_date_in_range(date_str, start_date, end_date):
                reports.append((date_str, filename))
    
    return sorted(reports)

def find_thoughts(start_date, end_date):
    """查找本周的工作思考文件"""
    thoughts = []
    if not os.path.exists(THOUGHTS_DIR):
        return thoughts
    
    for filename in os.listdir(THOUGHTS_DIR):
        if filename.endswith(".md"):
            date_str = parse_date_from_filename(filename)
            if date_str and is_date_in_range(date_str, start_date, end_date):
                thoughts.append((date_str, filename))
    
    return sorted(thoughts)

def find_meeting_notes(start_date, end_date):
    """查找本周的会议纪要文件"""
    meetings = []
    if not os.path.exists(MEETING_NOTES_DIR):
        return meetings
    
    for filename in os.listdir(MEETING_NOTES_DIR):
        if filename.endswith(".md"):
            date_str = parse_date_from_filename(filename)
            if date_str and is_date_in_range(date_str, start_date, end_date):
                meetings.append((date_str, filename))
    
    return sorted(meetings)

def extract_content_from_file(filepath):
    """从文件中提取内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败 {filepath}: {e}")
        return ""

def extract_work_items_from_daily(content, filename, date_str):
    """从日报中提取工作事项"""
    items = []
    
    # 匹配 "### 1. [标题]" 格式
    pattern = r'###\s*\d+\.\s*(.+?)\n\*\*核心内容\*\*：(.+?)(?=\n\*\*来源|$)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for title, core_content in matches:
        # 将核心内容按句号或分号拆分成要点
        points = []
        # 先用句号拆分，如果结果太长再用分号拆分
        raw_sentences = re.split(r'[。]', core_content.strip())
        for s in raw_sentences:
            s = s.strip()
            if not s:
                continue
            # 如果句子太长（包含分号），再拆分
            if '；' in s or ';' in s:
                sub_points = re.split(r'[；;]', s)
                for sub in sub_points:
                    sub = sub.strip()
                    if sub and len(sub) > 5:
                        if not sub.endswith('。') and not sub.endswith('.'):
                            sub += '。'
                        points.append(sub)
            else:
                if s and len(s) > 5:
                    if not s.endswith('。') and not s.endswith('.'):
                        s += '。'
                    points.append(s)
        
        # 格式化为列表
        formatted_content = '\n'.join([f"- {p}" for p in points[:4]])
        
        items.append({
            "title": title.strip(),
            "content": formatted_content,
            "source": filename.replace(".md", ""),
            "source_type": "daily",
            "date": date_str
        })
    
    return items

def extract_thoughts_items(content, filename, date_str):
    """从工作思考中提取事项 - 按主要章节拆分，保持列表结构"""
    items = []
    
    # 去掉 frontmatter
    clean_content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)
    
    # 提取所有二级标题 (##) 作为独立事项
    sections = re.split(r'\n##\s+', clean_content)
    
    for section in sections[1:]:  # 跳过第一个（通常是 frontmatter 后的内容）
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        # 第一行是标题
        title = lines[0].strip()
        # 清理标题
        title = re.sub(r'^#+\s*', '', title).strip()
        
        # 提取要点列表
        points = []
        in_table = False
        in_code = False
        
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            if line.startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            if line.startswith('|'):
                in_table = True
                continue
            if in_table and not line.startswith('|'):
                in_table = False
                continue
            if in_table:
                continue
            # 跳过标签行
            if line.startswith('tags:') or line.startswith('- "#'):
                continue
            # 提取列表项
            if line.startswith('- ') or line.startswith('* '):
                point = line[2:].strip()
                point = re.sub(r'\*\*', '', point)
                if point and len(point) > 10:
                    if not point.endswith('。') and not point.endswith('.') and not point.endswith('：'):
                        point += '。'
                    points.append(point)
        
        if title and points:
            # 保持为列表格式
            summary = '\n'.join([f"- {p}" for p in points[:5]])
            items.append({
                "title": title,
                "content": summary,
                "source": filename.replace(".md", ""),
                "source_type": "thoughts",
                "date": date_str
            })
    
    # 如果没有提取到章节，把整个文件作为一个事项
    if not items:
        title_match = re.search(r'^#\s*(.+)$', clean_content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else filename.replace(".md", "")
        title = re.sub(r'^#+\s*', '', title).strip()
        
        # 提取要点列表
        points = []
        for line in clean_content.split('\n'):
            line = line.strip()
            if line.startswith('- ') or line.startswith('* '):
                point = line[2:].strip()
                point = re.sub(r'\*\*', '', point)
                if point and len(point) > 10:
                    if not point.endswith('。') and not point.endswith('.') and not point.endswith('：'):
                        point += '。'
                    points.append(point)
        
        if points:
            summary = '\n'.join([f"- {p}" for p in points[:6]])
            items.append({
                "title": title,
                "content": summary,
                "source": filename.replace(".md", ""),
                "source_type": "thoughts",
                "date": date_str
            })
    
    return items

def extract_meeting_items(content, filename, date_str):
    """从会议纪要中提取事项 - 按主要章节拆分，保持列表结构"""
    items = []
    
    # 去掉 frontmatter
    clean_content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)
    
    # 提取所有二级/三级标题作为独立事项
    sections = re.split(r'\n###?\s+', clean_content)
    
    for section in sections[1:]:  # 跳过第一个
        lines = section.strip().split('\n')
        if not lines:
            continue
        
        title = lines[0].strip()
        title = re.sub(r'^#+\s*', '', title).strip()
        
        # 提取要点列表，保持为列表格式
        points = []
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            if line.startswith('```') or line.startswith('|'):
                continue
            if line.startswith('tags:') or line.startswith('- "#'):
                continue
            # 提取列表项
            if line.startswith('- ') or line.startswith('* '):
                point = line[2:].strip()
                point = re.sub(r'\*\*', '', point)
                # 确保以句号结尾
                if point and len(point) > 10:
                    if not point.endswith('。') and not point.endswith('.') and not point.endswith('：'):
                        point += '。'
                    points.append(point)
        
        if title and points:
            # 保持为列表，不要合并
            summary = '\n'.join([f"- {p}" for p in points[:5]])
            items.append({
                "title": title,
                "content": summary,
                "source": filename.replace(".md", ""),
                "source_type": "meeting",
                "date": date_str
            })
    
    # 如果没有提取到章节，把整个文件作为一个事项
    if not items:
        title_match = re.search(r'^#\s*(.+)$', clean_content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else filename.replace(".md", "")
        title = re.sub(r'^#+\s*', '', title).strip()
        
        # 提取要点列表
        points = []
        for line in clean_content.split('\n'):
            line = line.strip()
            if line.startswith('- ') or line.startswith('* '):
                point = line[2:].strip()
                point = re.sub(r'\*\*', '', point)
                if point and len(point) > 10:
                    if not point.endswith('。') and not point.endswith('.') and not point.endswith('：'):
                        point += '。'
                    points.append(point)
        
        if points:
            summary = '\n'.join([f"- {p}" for p in points[:6]])
            items.append({
                "title": title,
                "content": summary,
                "source": filename.replace(".md", ""),
                "source_type": "meeting",
                "date": date_str
            })
    
    return items

def categorize_item(title, content):
    """根据关键词对事项进行分类"""
    text = (title + " " + content).lower()
    
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword.lower() in text)
        if score > 0:
            scores[category] = score
    
    if scores:
        return max(scores, key=scores.get)
    return "其他"

def deduplicate_items(items):
    """去重：合并相似事项"""
    # 按标题相似度分组
    groups = defaultdict(list)
    
    for item in items:
        # 提取核心关键词作为分组键
        title_lower = item["title"].lower()
        
        # 找到匹配的组
        matched = False
        for key in list(groups.keys()):
            # 简单相似度：共享关键词
            key_words = set(key.lower().split())
            title_words = set(title_lower.split())
            common = key_words & title_words
            
            if len(common) >= 2 or (len(common) >= 1 and len(common) / max(len(key_words), len(title_words)) > 0.3):
                groups[key].append(item)
                matched = True
                break
        
        if not matched:
            groups[item["title"]] = [item]
    
    # 合并每组
    merged = []
    for key, group_items in groups.items():
        if len(group_items) == 1:
            merged.append(group_items[0])
        else:
            # 优先使用工作思考，其次是会议纪要
            priority_order = {"thoughts": 0, "meeting": 1, "daily": 2}
            sorted_items = sorted(group_items, key=lambda x: priority_order.get(x["source_type"], 3))
            
            # 使用优先级最高的作为主要项
            primary = sorted_items[0]
            
            # 合并来源
            all_sources = list(set([item["source"] for item in group_items]))
            primary["source"] = all_sources[0]  # 使用主要来源
            primary["all_sources"] = all_sources
            
            merged.append(primary)
    
    return merged

def extract_next_steps(daily_reports):
    """从日报中提取下周行动项"""
    next_steps = []
    
    for date_str, filename in daily_reports:
        filepath = os.path.join(DAILY_REPORTS_DIR, filename)
        content = extract_content_from_file(filepath)
        
        # 查找"下一步汇总"部分
        match = re.search(r'##\s*二、下一步汇总(.+?)(?=##|$)', content, re.DOTALL)
        if match:
            steps_text = match.group(1)
            steps = [s.strip('- ').strip() for s in steps_text.split('\n') if s.strip().startswith('-')]
            next_steps.extend(steps)
    
    # 去重
    seen = set()
    unique_steps = []
    for step in next_steps:
        if step and step not in seen:
            seen.add(step)
            unique_steps.append(step)
    
    return unique_steps[:15]  # 限制数量

def generate_weekly_report(start_date, end_date, daily_reports, thoughts, meetings):
    """生成周报内容"""
    all_items = []
    sources = []
    
    # 提取日报内容
    for date_str, filename in daily_reports:
        filepath = os.path.join(DAILY_REPORTS_DIR, filename)
        content = extract_content_from_file(filepath)
        items = extract_work_items_from_daily(content, filename, date_str)
        all_items.extend(items)
        sources.append(filename.replace(".md", ""))
    
    # 提取工作思考
    for date_str, filename in thoughts:
        filepath = os.path.join(THOUGHTS_DIR, filename)
        content = extract_content_from_file(filepath)
        items = extract_thoughts_items(content, filename, date_str)
        all_items.extend(items)
        sources.append(filename.replace(".md", ""))
    
    # 提取会议纪要
    for date_str, filename in meetings:
        filepath = os.path.join(MEETING_NOTES_DIR, filename)
        content = extract_content_from_file(filepath)
        items = extract_meeting_items(content, filename, date_str)
        all_items.extend(items)
        sources.append(filename.replace(".md", ""))
    
    # 去重
    all_items = deduplicate_items(all_items)
    
    # 按类别分组
    categorized = defaultdict(list)
    for item in all_items:
        category = categorize_item(item["title"], item["content"])
        categorized[category].append(item)
    
    # 生成报告
    report = []
    
    # 各业务板块
    category_order = ["产品开发", "客户项目", "数据分析", "产品设计", "团队管理", "战略规划", "其他"]
    
    for i, category in enumerate(category_order, 1):
        if category not in categorized or not categorized[category]:
            continue
        
        report.append(f"## {['一', '二', '三', '四', '五', '六', '七'][i-1]}、{category}")
        report.append("")
        
        for j, item in enumerate(categorized[category], 1):
            # 格式化日期显示
            date_obj = datetime.strptime(item["date"], "%Y-%m-%d")
            date_display = f"{date_obj.month}月{date_obj.day}日"
            
            # 提取标题（去掉日期部分）
            title = item["title"]
            
            report.append(f"**{j}. {title}（{date_display}）**")
            
            # 清理内容：去掉 markdown 标题、表格、代码块
            clean_content = item["content"]
            # 去掉表格行
            clean_content = re.sub(r'\n?\|[^\n]+\|[^\n]*', '', clean_content)
            # 去掉 markdown 标题
            clean_content = re.sub(r'^#+\s*', '', clean_content, flags=re.MULTILINE)
            # 去掉代码块
            clean_content = re.sub(r'```[\s\S]*?```', '', clean_content)
            clean_content = clean_content.strip()
            
            # 将内容拆分为要点
            content_lines = [line.strip() for line in clean_content.split('\n') if line.strip()]
            
            # 内容已经是处理过的要点列表（带 - 前缀），直接解析
            points = []
            
            for line in clean_content.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    point = line[2:].strip()
                    # 清理 markdown 格式
                    point = re.sub(r'\*\*', '', point)
                    if point and len(point) > 5:
                        points.append(point)
            
            # 如果没有提取到要点，尝试按句子拆分
            if not points:
                raw_points = re.split(r'[。]', clean_content)
                for point in raw_points:
                    point = point.strip()
                    if not point or len(point) < 10:
                        continue
                    if point.lower() == item["title"].lower():
                        continue
                    if point.startswith('文件摘要：'):
                        point = point[5:].strip()
                    point = re.sub(r'\*\*', '', point)
                    point = re.sub(r'^[-*]+\s*', '', point)
                    point = re.sub(r'^#+\s*', '', point)
                    point = re.sub(r'\s+', ' ', point)
                    
                    if len(point) > 10:
                        points.append(point)
                    
                    if len(points) >= 4:
                        break
            
            # 如果还是没有，使用内容摘要
            if not points:
                summary = clean_content[:150] + "..." if len(clean_content) > 150 else clean_content
                summary = re.sub(r'\*\*', '', summary)
                summary = re.sub(r'^[-*]+\s*', '', summary)
                points = [summary]
            
            for point in points[:4]:
                report.append(f"- {point}")
            
            report.append("")
        
        report.append("---")
        report.append("")
    
    # 下周重点
    next_steps = extract_next_steps(daily_reports)
    
    if next_steps:
        report.append("## 下周重点")
        report.append("")
        
        # 按相似度分组
        step_groups = defaultdict(list)
        for step in next_steps:
            # 简单分类
            if any(kw in step.lower() for kw in ["sengkang", "proposal", "客户", "项目"]):
                step_groups["客户项目"].append(step)
            elif any(kw in step.lower() for kw in ["oyen", "challenge", "设计", "ui", "ux"]):
                step_groups["产品设计"].append(step)
            elif any(kw in step.lower() for kw in ["21天", "习惯", "routines", "hi", "health index"]):
                step_groups["产品开发"].append(step)
            elif any(kw in step.lower() for kw in ["数据", "分析", "bi", "uag"]):
                step_groups["数据分析"].append(step)
            else:
                step_groups["其他事项"].append(step)
        
        for category, steps in step_groups.items():
            if steps:
                report.append(f"**{category}**")
                for step in steps[:5]:  # 每个类别最多 5 条
                    report.append(f"- {step}")
                report.append("")
    
    # 来源汇总
    report.append("---")
    report.append("")
    report.append("*来源：Obsidian 知识库*")
    
    unique_sources = list(set(sources))
    for source in sorted(unique_sources):
        report.append(f"- [[{source}]]")
    
    return '\n'.join(report), len(all_items), len(daily_reports), len(thoughts), len(meetings)

def save_report(content, start_date, end_date):
    """保存周报到文件"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    start_str = format_date(start_date)
    end_str = format_date(end_date)
    filename = f"{start_str}~{end_str} EVYD周报.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def main():
    """主函数"""
    # 获取本周日期范围
    start_date, end_date = get_week_range()
    
    print(f"生成本周周报：{format_date(start_date)} ~ {format_date(end_date)}")
    print(f"Vault 路径：{VAULT_PATH}")
    
    # 查找三个来源的文件
    daily_reports = find_daily_reports(start_date, end_date)
    thoughts = find_thoughts(start_date, end_date)
    meetings = find_meeting_notes(start_date, end_date)
    
    print(f"\n找到文件：")
    print(f"  - 日报：{len(daily_reports)} 份")
    print(f"  - 工作思考：{len(thoughts)} 篇")
    print(f"  - 会议纪要：{len(meetings)} 个")
    
    # 判断是否有内容
    total_sources = len(daily_reports) + len(thoughts) + len(meetings)
    
    if total_sources == 0:
        print("\n老板，本周没有工作记录 📋")
        return
    
    # 生成周报
    report_content, item_count, daily_count, thoughts_count, meetings_count = generate_weekly_report(
        start_date, end_date, daily_reports, thoughts, meetings
    )
    
    # 保存文件
    filepath = save_report(report_content, start_date, end_date)
    
    # 汇报
    print(f"\n老板，周报已生成！✅")
    print(f"文件位置：{filepath}")
    print(f"\n本周汇总统计：")
    print(f"  - 日报：{daily_count} 份")
    print(f"  - 工作思考：{thoughts_count} 篇")
    print(f"  - 会议纪要：{meetings_count} 个")
    print(f"  - 去重后事项：{item_count} 条")
    print(f"\n已按业务板块整理完成～ 🦐👓")

if __name__ == "__main__":
    main()
