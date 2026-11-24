#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量套用 brand 区域修复到所有 HTML：
- --sidebar-w 262px → 280px
- .brand-t font-size 17px → 16px
- .brand-name{white-space:nowrap} 替换为 zh/en 分别控制
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))


def fix(path):
    t = io.open(path, encoding="utf-8").read()
    orig = t
    changes = []

    # 1. sidebar width
    t2, n = re.subn(r'--sidebar-w:\s*262px\s*;', '--sidebar-w:280px;', t)
    if n:
        t = t2
        changes.append(f"sidebar-w ×{n}")

    # 2. brand-t font-size 17px → 16px (只替换 .brand-t 里的)
    t2, n = re.subn(
        r'(\.brand-t\{[^}]*?font-size:)17px',
        r'\g<1>16px',
        t
    )
    if n:
        t = t2
        changes.append(f"brand-t font-size ×{n}")

    # 3. brand-name CSS 替换
    #    旧：.brand-name{white-space:nowrap}
    #    新：.brand-t .zh-only .brand-name{white-space:nowrap}
    #        .brand-t .en-only .brand-name{white-space:normal}
    t2, n = re.subn(
        r'\.brand-name\{white-space:nowrap\}',
        '.brand-t .zh-only .brand-name{white-space:nowrap}\n'
        '.brand-t .en-only .brand-name{white-space:normal}',
        t
    )
    if n:
        t = t2
        changes.append(f"brand-name CSS ×{n}")

    if t != orig:
        io.open(path, "w", encoding="utf-8").write(t)
    return changes


def main():
    updated = 0
    for fname in sorted(os.listdir(SITE)):
        if not fname.endswith(".html"):
            continue
        c = fix(os.path.join(SITE, fname))
        if c:
            updated += 1
            print(f"  ✓ {fname}: {', '.join(c)}")
        else:
            print(f"  - {fname}")
    print(f"\n更新 {updated} 个文件")


if __name__ == "__main__":
    main()
