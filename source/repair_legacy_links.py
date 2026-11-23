#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把旧 MyCi 正文中已失效的本页小节链接接回原官方文章小节。"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))
ART_RE = re.compile(r'<div class="art" id="a-[\w.\-]+">.*?'
                    r'(?=<div class="art" id="a-|</article>)', re.S)
SRC_RE = re.compile(r'<div class="art-src"><a href="([^"]+)"')
LOCAL_HREF = re.compile(r'href="#([^"]+)"')


def repair(name):
    path = os.path.join(SITE, name)
    text = io.open(path, encoding="utf-8").read()
    ids = set(re.findall(r'\bid="([^"]+)"', text))
    changes = 0
    for match in reversed(list(ART_RE.finditer(text))):
        block = match.group(0)
        source = SRC_RE.search(block)
        if not source:
            continue
        base = source.group(1)

        def external(match):
            nonlocal changes
            fragment = match.group(1)
            if fragment in ids:
                return match.group(0)
            if fragment.lower().startswith("a-"):
                return match.group(0)
            changes += 1
            return f'href="{base}#{fragment}"'

        new_block = LOCAL_HREF.sub(external, block)
        text = text[:match.start()] + new_block + text[match.end():]
    if changes:
        io.open(path, "w", encoding="utf-8").write(text)
    return changes


def main():
    total = 0
    for name in sorted(os.listdir(SITE)):
        if not name.endswith(".html"):
            continue
        count = repair(name)
        if count:
            print(f"  {name}: {count} 个原文小节链接已接回官方页面")
            total += count
    print(f"旧文链接修复完成：{total} 处")


if __name__ == "__main__":
    main()
