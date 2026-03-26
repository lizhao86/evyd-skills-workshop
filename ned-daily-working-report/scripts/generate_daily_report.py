#!/usr/bin/env python3
"""
Ned 每日工作报告生成器
从 Obsidian 读取当天会议纪要和个人日记，生成日报并保存到 24-Work-周报汇总
"""

import os
import re
from datetime import datetime
from pathlib import Path

# 配置路径
MEETING_NOTES_DIR = "/Users/Li.ZHAO/我赵立的仓库/21-Work-会议纪要 💼"
DIARY_DIR = "/Users/Li.ZHAO/我赵立的仓库/10-Notes-晨夕日记 📝"
OUTPUT_DIR = "/Users/Li.ZHAO/我赵立的仓库/24-Work-周报汇总"

def get_today_date():
    """获取今天日期，格式：2026-03-10"""
    return datetime.now().strftime("%Y-%m-%d")

def find_meeting_notes(date_str):
    """查找当天的会议纪要文件"""
    meeting_notes = []
    if not os.path.exists(MEETING_NOTES_DIR):
        return meeting_notes
    
    for filename in os.listdir(MEETING_NOTES_DIR):
        if filename.endswith(".md") and date_str in filename:
            meeting_notes.append(filename)
    
    return sorted(meeting_notes)

def find_diary_entry(date_str):
    """查找当天的日记文件"""
    # 解析日期
    year = date_str.split("-")[0]
    month = date_str.split("-")[1]
    
    diary_path = os.path.join(DIARY_DIR, year, month)
    diary_files = []
    
    if os.path.exists(diary_path):
        for filename in os.listdir(diary_path):
            if filename.endswith(".md") and date_str in filename:
                diary_files.append(os.path.join(diary_path, filename))
    
    return diary_files

def extract_content_from_file(filepath):
    """从文件中提取核心内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取关键部分
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('# ') or line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = line.strip('# ').strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return content, sections

def summarize_meeting(filepath):
    """总结会议纪要的核心内容"""
    content, sections = extract_content_from_file(filepath)
    
    # 尝试从不同部分提取核心内容
    summary = ""
    
    # 优先使用 Quick Takeaways
    if "Quick Takeaways" in sections:
        summary = sections["Quick Takeaways"].strip()
    elif "会议概述" in sections:
        summary = sections["会议概述"].strip()
    else:
        # 如果没有明确部分，取前 3 段非空内容
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.startswith('---') and not p.startswith('tags:')]
        summary = '\n\n'.join(paragraphs[:3])
    
    # 限制长度
    if len(summary) > 500:
        summary = summary[:500] + "..."
    
    return summary

def extract_next_steps(meeting_notes):
    """从会议纪要中提取下一步行动"""
    next_steps = []
    
    for filename in meeting_notes:
        filepath = os.path.join(MEETING_NOTES_DIR, filename)
        content, sections = extract_content_from_file(filepath)
        
        # 查找待办事项
        if "待完成" in sections:
            items = sections["待完成"].strip().split('\n')
            next_steps.extend([item.strip('- ').strip() for item in items if item.strip()])
        
        if "Action Items" in sections:
            items = sections["Action Items"].strip().split('\n')
            next_steps.extend([item.strip('- ').strip() for item in items if item.strip() and not item.startswith('- ')])
    
    return next_steps[:10]  # 限制最多 10 条

def generate_report(date_str, meeting_notes, diary_files):
    """生成日报内容"""
    report = []
    
    # 工作流水账
    report.append("## 一、工作流水账")
    report.append("")
    
    for i, filename in enumerate(meeting_notes, 1):
        # 提取不带 .md 的文件名用于引用
        ref_name = filename.replace(".md", "")
        
        # 提取会议标题（从文件名）
        title_parts = filename.split(" ")
        if len(title_parts) > 2:
            title = " ".join(title_parts[2:]).replace(".md", "")
        else:
            title = ref_name
        
        # 总结会议内容
        filepath = os.path.join(MEETING_NOTES_DIR, filename)
        summary = summarize_meeting(filepath)
        
        # 生成条目
        report.append(f"### {i}. {title}")
        report.append(f"**核心内容**：{summary}")
        report.append(f"**来源**：[[{ref_name}]]")
        report.append("")
    
    # 下一步汇总
    next_steps = extract_next_steps(meeting_notes)
    
    if next_steps:
        report.append("## 二、下一步汇总")
        report.append("")
        for step in next_steps:
            report.append(f"- {step}")
    
    return '\n'.join(report)

def save_report(content, date_str):
    """保存日报到文件"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{date_str} EVYD 日报.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def main():
    """主函数"""
    date_str = get_today_date()
    
    # 查找文件
    meeting_notes = find_meeting_notes(date_str)
    diary_files = find_diary_entry(date_str)
    
    # 判断是否有工作内容
    if not meeting_notes:
        print("今天没有工作记录 📋")
        return
    
    # 生成日报
    report_content = generate_report(date_str, meeting_notes, diary_files)
    
    # 保存文件
    filepath = save_report(report_content, date_str)
    
    print(f"日报已生成！✅")
    print(f"文件位置：{filepath}")
    print(f"今天共有 {len(meeting_notes)} 条工作记录，已汇总完成～ 🦐👓")

if __name__ == "__main__":
    main()
