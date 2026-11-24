#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量更新 24 个 HTML 的侧边栏品牌区：
- brand-t 主标题改为完整名称 "Prokit/CI Tools(旧）完全指南"
- 其中 "Prokit/CI Tools(旧）" 加 white-space:nowrap 确保不换行
- 英文 brand-t 同步改为 "ProKit / CI Tools (legacy) Complete Guide"
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

OLD_HTML_PAT = re.compile(
    r'<div class="brand-t">'
    r'(<span class="zh-only">ProKit\s*/\s*CI Tools（旧）</span>)'
    r'(<span class="en-only">ProKit\s*/\s*CI Tools \(legacy\)</span>)'
    r'</div>'
)

NEW_HTML = (
    r'<div class="brand-t">'
    r'<span class="zh-only"><span class="brand-name">Prokit/CI Tools(旧）</span>完全指南</span>'
    r'<span class="en-only"><span class="brand-name">ProKit / CI Tools (legacy)</span> Complete Guide</span>'
    r'</div>'
)

# CSS: 匹配 .brand-t{...} 的结束 '}'，在其后插入 .brand-name 规则
# 用更宽松的匹配：找 .brand-t{ 到对应的 }
BRAND_T_BLOCK = re.compile(
    r'(\.brand-t\{[^}]*\})'
)

BRAND_NAME_CSS = "\n.brand-name{white-space:nowrap}\n"


def fix_file(path):
    t = io.open(path, encoding="utf-8").read()
    original = t
    changes = []

    # 1. 替换 HTML
    new_t, n = OLD_HTML_PAT.subn(NEW_HTML, t)
    if n > 0:
        t = new_t
        changes.append(f"HTML brand-t ×{n}")

    # 2. 注入 CSS（只在没 .brand-name 规则时注入）
    if ".brand-name" not in t:
        # 在 .brand-t{...} 闭合 } 之后插入
        def _css_repl(m):
            return m.group(1) + BRAND_NAME_CSS
        new_t2, m2 = BRAND_T_BLOCK.subn(_css_repl, t, count=1)
        if m2 > 0:
            t = new_t2
            changes.append("CSS .brand-name")

    if t != original:
        io.open(path, "w", encoding="utf-8").write(t)
        return changes
    return None


def main():
    html_files = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    updated = 0
    for fname in html_files:
        path = os.path.join(SITE, fname)
        changes = fix_file(path)
        if changes:
            updated += 1
            print(f"  ✓ {fname}: {', '.join(changes)}")
        else:
            print(f"  - {fname}: 无匹配")
    print(f"\n完成：{updated}/{len(html_files)} 个文件更新")


if __name__ == "__main__":
    main()
