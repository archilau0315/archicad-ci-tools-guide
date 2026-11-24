#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清查全站交叉引用：哪些已包装成 xref 链接、哪些是裸文本、哪些锚点不存在。"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

ZH = re.compile(r'(?:见|参见|详见|更多细节见|另请参见|请参见|详见|详见第)\s*(第\s*\d+(?:\.\d+)*\s*节)')
EN = re.compile(r'\b(?:see|refer to)\s+(?:sections?\s+)?(\d+(?:\.\d+)+)', re.I)

results = []
html_files = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))

for fname in html_files:
    text = io.open(os.path.join(SITE, fname), encoding="utf-8").read()

    # 收集本页所有 h3 id
    h3_ids = set(re.findall(r'<h3\b[^>]*\sid="(s-[\d\-]+)"', text))

    # 收集本页所有 xref href
    xref_hrefs = set(re.findall(r'<a[^>]*class="[^"]*xref[^"]*"[^>]*href="(#s-[\d\-]+)"', text))

    # 裸文本检查：找"第 X.X.X 节"中带小数点的
    for m in re.finditer(r'第\s*(\d+(?:\.\d+)+)\s*节', text):
        num = m.group(1)
        pos = m.start()
        # 看前面有没有 <a ... class="xref">
        pre = text[max(0,pos-200):pos]
        # 往前找最近一个 <a 及其 class
        last_a = pre.rfind("<a ")
        if last_a >= 0:
            tail = pre[last_a:]
            is_xref = 'class="xref"' in tail.split(">")[0] if ">" in tail else False
            already_in_a = False
            # 检查当前位置是否仍在这个 <a> 的闭合 </a> 之前
            if ">" in tail:
                from_a_open = tail.split(">", 1)[1]
                close = from_a_open.find("</a>")
                already_in_a = close == -1 or close > 0
            if is_xref and already_in_a:
                continue  # 已包装

        target = "#s-" + num.replace(".", "-")
        if target not in xref_hrefs:
            anchor_exists = target.lstrip("#") in h3_ids
            results.append((fname, pos, "ZH", num, "裸文本" + ("(锚点不存在!)" if not anchor_exists else "")))

    # 裸文本检查：英文 "section X.X.X"
    # 先用占位符把已有的 <a ... xref ...>...</a> 替换掉
    protected = re.sub(r'<a\b[^>]*class="[^"]*xref[^"]*"[^>]*>.*?</a>', " \u0000XREF\u0000 ", text, flags=re.S)

    for m in re.finditer(r'\bsection\s+(\d+(?:\.\d+)+)', protected, re.I):
        num = m.group(1)
        pos = m.start()
        # 看位置前后 30 字符内有没有占位符
        chunk = protected[max(0,pos-30):pos+30]
        if "\u0000XREF\u0000" in chunk:
            continue  # 已包装

        target = "#s-" + num.replace(".", "-")
        anchor_exists = target.lstrip("#") in h3_ids
        results.append((fname, pos, "EN", num, "裸文本" + ("(锚点不存在!)" if not anchor_exists else "")))

# 输出
print(f"{'='*70}\n清查结果：共 {len(results)} 处未包装的裸文本交叉引用\n{'='*70}")
for fname, pos, lang, num, note in results:
    print(f"  {fname:40s} {lang}  {num:12s}  {note}")

# 汇总
from collections import Counter
per_file = Counter(r[0] for r in results)
if per_file:
    print(f"\n按文件汇总：")
    for f, c in sorted(per_file.items(), key=lambda x: -x[1]):
        print(f"  {f}: {c} 处")
else:
    print("\n全部交叉引用都已包装成 xref ✅")
