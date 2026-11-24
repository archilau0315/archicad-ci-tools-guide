#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""报告：全站正文顶级 h2/h3 裸中文（不含 zh-only 包裹）"""
import io, os, re

SITE = r"e:\works\Aidev\Kbitai绝对安全\kbitai_com_cn\resources\AC_Tutorial\ci_tools\site"
HAS_ZH = re.compile(r'[\u4e00-\u9fff]')

# 只列 "明显是 UI 标签" 的 —— 标题较短 (<20字) 且不是正文段落
skip_if_longer_than = 20

total_issues = 0
for fname in sorted(os.listdir(SITE)):
    if not fname.endswith(".html"):
        continue
    t = io.open(os.path.join(SITE, fname), encoding="utf-8").read()
    m_main = re.search(r'<main\b[^>]*>([\s\S]*?)</main>', t)
    if not m_main:
        continue
    inner = m_main.group(1)
    pattern = re.compile(r'<(h[23])(\s[^>]*)?>([\s\S]*?)</\1>', re.S)
    page_issues = []
    for m in pattern.finditer(inner):
        tag = m.group(1)
        full_open = m.group(0)[:m.group(0).find('>')+1]
        content = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        if not HAS_ZH.search(content):
            continue
        if 'zh-only' in m.group(0):
            continue
        if len(content) > skip_if_longer_than:
            continue
        # 跳过带徽标的（span class="pkg"）
        if 'class="pkg' in m.group(0):
            continue
        page_issues.append((tag, content))
    if page_issues:
        print(f"\n=== {fname} ===")
        for tag, content in page_issues:
            print(f"  <{tag}>  裸中文:  {content}")
        total_issues += len(page_issues)

print(f"\n{'='*50}")
print(f"共 {total_issues} 处正文顶级标题裸中文")
