#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""brand 区域 zh-only 拆两行：
- 把 "完全指南" / "Complete Guide" 裸文本套 span.brand-sub
- CSS: zh-only 里 brand-name 和 brand-sub 都是 block
       brand-sub 字号小一号 + muted 色
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

# HTML 替换：zh-only / en-only 里的 trailing 文本套 <span class="brand-sub">
HTML_ZH = re.compile(
    r'(<span class="zh-only"><span class="brand-name">[^<]+</span>)([^<]+)(</span>)'
)
HTML_EN = re.compile(
    r'(<span class="en-only"><span class="brand-name">[^<]+</span>)(\s*Complete Guide)(</span>)'
)

# CSS 清理 + 注入
OLD_RULES = [
    r'\.brand-t \.zh-only\{white-space:nowrap\}\s*',
    r'\.brand-t \.en-only\{white-space:normal\}\s*',
]

NEW_CSS = (
    "\n/* brand 区域：zh-only 两行 */\n"
    ".brand-t .zh-only{white-space:normal;display:block}\n"
    ".brand-t .zh-only .brand-name{display:block;font-size:15px;line-height:1.25}\n"
    ".brand-t .zh-only .brand-sub{display:block;font-size:12px;font-weight:500;color:var(--muted);margin-top:2px;line-height:1.2}\n"
    ".brand-t .en-only{white-space:normal;display:block}\n"
    ".brand-t .en-only .brand-name{display:block;font-size:15px;line-height:1.25}\n"
    ".brand-t .en-only .brand-sub{display:block;font-size:12px;font-weight:500;color:var(--muted);margin-top:2px;line-height:1.2}\n"
)


def fix(path):
    t = io.open(path, encoding="utf-8").read()
    orig = t

    # 1. 替换 HTML
    t = HTML_ZH.sub(
        lambda m: m.group(1) + '<span class="brand-sub">' + m.group(2).strip() + '</span>' + m.group(3),
        t
    )
    t = HTML_EN.sub(
        lambda m: m.group(1) + '<span class="brand-sub">' + m.group(2).strip() + '</span>' + m.group(3),
        t
    )

    # 2. 清旧 CSS
    for pat in OLD_RULES:
        t = re.sub(pat, '', t)

    # 3. 新 CSS 注入：在 .brand-t{...} 之后
    if '.brand-t .zh-only{white-space:normal;display:block}' not in t:
        t = re.sub(
            r'(\.brand-t\{[^}]*\})',
            r'\g<1>' + NEW_CSS.replace('\\', '\\\\'),
            t,
            count=1
        )

    if t != orig:
        io.open(path, "w", encoding="utf-8").write(t)
        return True
    return False


def main():
    u = 0
    for f in sorted(os.listdir(SITE)):
        if f.endswith(".html") and fix(os.path.join(SITE, f)):
            u += 1
            print(f"  ✓ {f}")
    print(f"\n更新 {u} 个文件")


if __name__ == "__main__":
    main()
