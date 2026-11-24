#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""彻底修复 brand-t 区域 CSS：
1. 清理错乱的叠层选择器（上一次替换把 .brand-t .zh-only 重复了）
2. .brand-t .zh-only 整体 white-space:nowrap（确保"Prokit/CI Tools(旧）完全指南"一行）
3. .brand-t .en-only 允许换行（英文长）
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))


def fix(path):
    t = io.open(path, encoding="utf-8").read()
    orig = t
    changes = 0

    # 1. 删掉所有已有的 .brand-t .zh-only .brand-name 和 .brand-t .en-only .brand-name 行
    #    （不管叠了多少层）
    t2, n = re.subn(
        r'\.brand-t \.zh-only(?:\s+\.brand-t\s+\.zh-only)*\s*\.brand-name\{[^}]*\}\s*',
        '', t
    )
    t2, n2 = re.subn(
        r'\.brand-t \.en-only(?:\s+\.brand-t\s+\.en-only)*\s*\.brand-name\{[^}]*\}\s*',
        '', t2
    )
    if n + n2:
        t = t2

    # 2. 在 .brand-t{...} 之后插入两条规则（如果没有的话）
    #    找 .brand-t{...} 的结束 }
    def _inject(m):
        # 已有的话跳过
        if '.brand-t .zh-only{white-space:nowrap}' in t:
            return m.group(0)
        return m.group(0) + "\n.brand-t .zh-only{white-space:nowrap}\n.brand-t .en-only{white-space:normal}"

    t2, n = re.subn(
        r'(\.brand-t\{[^}]*\})',
        _inject,
        t,
        count=1
    )
    if n:
        t = t2
        changes += 1

    if t != orig:
        io.open(path, "w", encoding="utf-8").write(t)
    return changes


def main():
    u = 0
    for f in sorted(os.listdir(SITE)):
        if not f.endswith(".html"):
            continue
        c = fix(os.path.join(SITE, f))
        if c:
            u += 1
            print(f"  ✓ {f}")
    print(f"\n更新 {u} 个文件")


if __name__ == "__main__":
    main()
