#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描全站中文文案在 EN 模式下是否仍可见。

原理：
  每个可见文本节点如果包含中文字符，必须被 <span class="zh-only"> 包裹，
  并且有一个对应的 <span class="en-only"> 英文版本在旁边。
  否则 EN 模式下该中文会泄露出来。

扫描范围：正文 h1/h2/h3、sidebar 导航条目、内容区 <li> 链接、
          .nav-h 分组标签、卡片标题/副标题等。
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

# 中文判断：含常见中文字符
HAS_ZH = re.compile(r'[\u4e00-\u9fff\(\)（），、。]')

# 跳过这些容器里的文本（代码块、style、script、link 标题 span.tg 里的数字等）
SKIP_PATTERNS = [
    r'<style[^>]*>.*?</style>',
    r'<script[^>]*>.*?</script>',
    r'<code[^>]*>.*?</code>',
    r'<pre[^>]*>.*?</pre>',
    r'<title>.*?</title>',
]


def strip_tags(s):
    """去掉所有 HTML 标签，保留文本"""
    return re.sub(r'<[^>]+>', '', s)


def scan_file(path):
    t = io.open(path, encoding="utf-8").read()

    # 预处理：用占位符保护跳过区域
    protected = t
    placeholders = {}
    for i, pat in enumerate(SKIP_PATTERNS):
        def _save(m, idx=i):
            k = f'\x00SK{idx}_{len(placeholders)}\x00'
            placeholders[k] = m.group(0)
            return k
        protected = re.sub(pat, _save, protected, flags=re.S)

    issues = []

    # 规则 A：被 zh-only 包裹的文本必须有同级 en-only
    # 找出所有 <span class="zh-only">...</span> 及其后续 <span class="en-only">...</span>
    # 统计数量差
    zh_only = list(re.finditer(r'<span class="zh-only"[^>]*>(.*?)</span>', protected, re.S))
    en_only = list(re.finditer(r'<span class="en-only"[^>]*>(.*?)</span>', protected, re.S))
    if len(zh_only) != len(en_only):
        issues.append(f"zh-only({len(zh_only)}) vs en-only({len(en_only)}) 数量不一致")

    # 规则 B：可见的中文文本，其祖先链必须有 zh-only 包裹
    # 简单做法：找所有"含中文且不在 zh-only 里"的文本块
    # 用 <p>、<h1>~<h4>、<li>、<a>、<div class="art"> 等作为容器
    containers = re.compile(
        r'<(h[1-4]|p|li|a|dt|dd)[^>]*>([\s\S]{0,500}?)</\1>'
        r'|<div class="[^"]*(?:art-h|card|feat|call|banner)[^"]*"[^>]*>([\s\S]{0,800}?)</div>'
        r'|<span class="(?:nav-h|card-t|card-s|feat-t|feat-s)[^"]*"[^>]*>([\s\S]{0,200}?)</span>',
        re.S
    )

    for m in containers.finditer(protected):
        block = m.group(0)
        plain = strip_tags(block).strip()
        if not plain or not HAS_ZH.search(plain):
            continue
        # 检查中文部分是否被 zh-only 包裹
        if 'zh-only' not in block:
            # 跳过：如果纯中文是被 label/placeholder 之类 HTML 属性包住
            # 或只是注释、或为空
            short = plain[:60].replace('\n', ' ')
            issues.append(f"  泄漏中文: {short}")

    return issues


def main():
    html_files = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    total = 0
    for fname in html_files:
        path = os.path.join(SITE, fname)
        issues = scan_file(path)
        if issues:
            print(f"\n=== {fname} ({len(issues)} 处) ===")
            for i in issues:
                print(i)
            total += len(issues)
    print(f"\n{'='*60}")
    print(f"共发现 {total} 处中文在 EN 模式下可能泄漏")


if __name__ == "__main__":
    main()
