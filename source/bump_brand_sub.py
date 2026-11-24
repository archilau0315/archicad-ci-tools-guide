#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 brand-sub（完全指南）字号从 12px 提到 14px，更显眼。"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

OLD = re.compile(
    r'(\.brand-t \.(?:zh-only|en-only) \.brand-sub\{[^}]*?)font-size:12px'
)


def fix(path):
    t = io.open(path, encoding="utf-8").read()
    orig = t
    t2, n = OLD.subn(r'\g<1>font-size:14px', t)
    if n:
        io.open(path, "w", encoding="utf-8").write(t2)
        return n
    return 0


u = 0
for f in sorted(os.listdir(SITE)):
    if not f.endswith(".html"):
        continue
    c = fix(os.path.join(SITE, f))
    if c:
        u += 1
print(f"更新 {u} 个文件")
