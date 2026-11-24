#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 index.html / all.html 工具分组 h2 的双语。

模式：
  <h2>Annotate · 文字格式 <span class="pill">5 篇</span></h2>
目标：
  <h2>Annotate · <span class="zh-only">文字格式</span> <span class="pill"><span class="zh-only block">5 篇</span><span class="en-only">5 articles</span></span></h2>
即：工具英文名保留，中文副标题 + pill 数字加 zh-only/en-only 双语。
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

PAT = re.compile(
    r'<h2>([A-Z][a-zA-Z+ /&-]+)\s*·\s*'   # 工具英文名
    r'([^\s]+(?:\s[^\s]+){0,4}?)'        # 中文副标题 (最多5词)
    r'\s*<span class="pill">(\d+)\s*篇</span></h2>'
)


def fix_file(path):
    t = io.open(path, encoding="utf-8").read()
    original = t
    changes = 0

    def repl(m):
        nonlocal changes
        en_tool = m.group(1).strip()
        zh_sub = m.group(2).strip()
        num = m.group(3)
        changes += 1
        return (
            f'<h2>{en_tool} · '
            f'<span class="zh-only">{zh_sub}</span> '
            f'<span class="pill">'
            f'<span class="zh-only block">{num} 篇</span>'
            f'<span class="en-only">{num} articles</span>'
            f'</span></h2>'
        )

    t2, n = PAT.subn(repl, t)
    if n > 0:
        t = t2
        io.open(path, "w", encoding="utf-8").write(t)
    return changes


def main():
    html_files = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    for fname in html_files:
        c = fix_file(os.path.join(SITE, fname))
        if c:
            print(f"  ✓ {fname}: {c} 处")


if __name__ == "__main__":
    main()
