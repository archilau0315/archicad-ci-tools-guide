# -*- coding: utf-8 -*-
"""给教程站里「基于旧版 Archicad 编写」的文章打版本角标。

背景：357 篇里有 23 篇标题自带版本号（AC19 3 篇、AC20 1 篇、AC22 17 篇、AC23 2 篇），
集中在 Cabinets（18 篇）。这些文章的操作步骤基于旧版界面，需要给读者一个显式提示。

做法：直接改 site/*.html（构建输入 clean.json / articles.json 已不在，无法重跑 build_site.py），
幂等：已有角标的块会跳过，可反复执行。

用法：
    python tools/add_version_badges.py [site目录]
"""
import io
import os
import re
import sys

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")

VER_RE = re.compile(r'ARCHICAD\s*(\d{2})|\bAC\s?(\d{2})\b', re.I)
# 只标 AC26 及更早：AC27 与 AC28 界面基本一致，标成"旧版"反而误导
MAX_OLD = 26
# 明确写给旧版、对当前版本已无操作价值的那几篇，标得更重
HISTORY_HINTS = ("及更早版本", "迁移到", "更新概览", "网络研讨会录像")

CSS = """
.vb{display:inline-block;margin-left:8px;padding:1px 6px;border-radius:4px;
  background:#f1e7d8;color:#8a5a1e;border:1px solid #e2d2ba;
  font-size:11px;font-weight:600;line-height:1.6;vertical-align:middle;
  letter-spacing:.02em;white-space:nowrap}
.vb-old{background:#f7e3e3;color:#9a3b3b;border-color:#e6c6c6}
.vb-note{margin:14px 0 0;padding:10px 14px;border-radius:10px;
  background:#fdf8f1;border:1px solid #f0e2cc;color:#7a5a2c;font-size:13.5px;line-height:1.7}
.vb-note b{color:#8a5a1e}
"""

NOTE = """  <p class="vb-note">
    <span class="zh-only">标 <b>AC19–AC23</b> 的文章基于旧版界面编写：功能思路仍通用，但按钮位置和菜单名可能与当前版本不同。</span>
    <span class="en-only">Articles tagged <b>AC19–AC23</b> were written for older interfaces — the concepts still apply, but UI paths may differ from the current version.</span>
  </p>"""


def badge_for(text):
    m = VER_RE.search(text)
    if not m:
        return ""
    ver = int(m.group(1) or m.group(2))
    if ver > MAX_OLD:
        return ""
    label = f"AC{ver}"
    cls = "vb vb-old" if any(h in text for h in HISTORY_HINTS) else "vb"
    title = "该文基于旧版界面，操作路径可能已变" if cls.endswith("old") else "基于该版本的界面编写"
    return f'<span class="{cls}" title="{title}">{label}</span>'


def process(path):
    html = io.open(path, encoding="utf-8").read()
    orig = html
    hits = 0

    # 1) 分册页：<div class="art" ...> 里的 h3 标题（按块切分，避免嵌套标签干扰）
    parts = html.split('<div class="art" id="a-')
    for i in range(1, len(parts)):
        chunk = parts[i]
        if 'class="vb' in chunk:
            continue
        def h3(m2):
            nonlocal hits
            inner = m2.group(2)
            b = badge_for(re.sub(r'<[^>]+>', '', inner))
            if not b:
                return m2.group(0)
            hits += 1
            return f'{m2.group(1)}{inner}{b}</h3>'
        parts[i] = re.sub(r'(<h3 class="(?:zh-only|en-only) block">)(.*?)</h3>', h3, chunk, flags=re.S)
    html = '<div class="art" id="a-'.join(parts)

    # 2) 全量索引：TOC 链接里的标题
    def toc_repl(m):
        nonlocal hits
        line = m.group(0)
        if 'class="vb' in line:
            return line
        def span(m2):
            nonlocal hits
            b = badge_for(re.sub(r'<[^>]+>', '', m2.group(2)))
            if not b:
                return m2.group(0)
            hits += 1
            return f'{m2.group(1)}{m2.group(2)}{b}</span>'
        return re.sub(r'(<span class="(?:zh-only|en-only)">)(.*?)</span>', span, line, flags=re.S)

    html = re.sub(r'<li><a href="[a-z]+\.html#a-\d+">.*?</a></li>', toc_repl, html, flags=re.S)

    # 3) 注入 CSS
    if ".vb{" not in html:
        html = html.replace("</style>", CSS + "</style>", 1)

    # 4) 有角标的分册页，在 hero 统计行下面加提示
    if '<p class="vb-note">' not in html and 'class="hero"' in html and 'class="vb' in html:
        html = re.sub(r'(<div class="meta">.*?</div>)', r'\1\n' + NOTE, html, count=1, flags=re.S)

    if html != orig:
        io.open(path, "w", encoding="utf-8").write(html)
    return hits


def main():
    total = 0
    for fn in sorted(os.listdir(SITE)):
        if not fn.endswith(".html"):
            continue
        n = process(os.path.join(SITE, fn))
        if n:
            print(f"  {fn:<26} 打标 {n // 2 if 'all.html' not in fn else n} 篇")
        total += n
    print(f"完成，共处理角标 {total} 处（中英各一份）")


if __name__ == "__main__":
    main()
