#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 AC30 官方手册内容重建 4 个 Core 工具页（P3b）

- 只替换 <article>…</article>，外壳、导航、样式保持不变
- 同步 hero 统计数字、all.html / index.html 的 Core 分组与全站篇数
- 图片使用本地 img/prokit/<tool>/，不引用官方直链

用法：python source/build_core_pages.py
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, HERE)
from core_content import CONTENT  # noqa: E402

NAMES = {"annotate": "Annotate", "transformer": "Transformer",
         "timetracker": "Time Tracker", "detail": "Detail Elements"}
ZH_NAMES = {"annotate": "文字格式", "transformer": "项目镜像",
            "timetracker": "工时统计", "detail": "二维详图"}
OLD_TOTAL, NEW_TOTAL = 422, 418
problems = []


def fig(path, cap):
    full = os.path.join(SITE, path.replace("/", os.sep))
    if not os.path.exists(full):
        problems.append("缺图 " + path)
    return (f'<figure><img src="{path}" alt="{cap}" loading="lazy">'
            f'<figcaption>{cap}</figcaption></figure>')


def render_blocks(blocks, lang):
    out = []
    for b in blocks:
        kind = b[0]
        if kind == "p":
            out.append("<p>%s</p>" % b[1 if lang == "zh" else 2])
        elif kind == "h4":
            out.append("<h4>%s</h4>" % b[1 if lang == "zh" else 2])
        elif kind == "ul":
            items = b[1] if lang == "zh" else b[2]
            out.append("<ul>" + "".join("<li>%s</li>" % x for x in items) + "</ul>")
        elif kind == "fig":
            out.append(fig(b[1], b[2] if lang == "zh" else b[3]))
        elif kind == "table":
            rows = b[1] if lang == "zh" else b[2]
            head = ("<tr><th>文件夹</th><th>数量</th><th>代表对象</th></tr>"
                    if lang == "zh" else
                    "<tr><th>Folder</th><th>Items</th><th>Examples</th></tr>")
            body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
            out.append('<div class="table-wrap"><table>%s%s</table></div>' % (head, body))
    return "\n".join(out)


def plain(text):
    return re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", text))


def render_article(a, idx):
    zh = render_blocks(a["blocks"], "zh")
    en = render_blocks(a["blocks"], "en")
    return f'''
<div class="art" id="a-{a["id"]}">
  <div class="art-h"><span class="no">{idx:02d}</span>
    <h3 class="zh-only block">{a["zh"]}</h3>
    <h3 class="en-only block">{a["en"]}</h3>
  </div>
  <div class="art-src"><span class="zh-only">来源：Graphisoft AC30 官方帮助 · {NAMES_FOR_SRC}</span><span class="en-only">Source: Graphisoft AC30 help · {NAMES_FOR_SRC}</span> · <a href="{a["src"]}" target="_blank" rel="noopener">原文 / original ↗</a></div>
  <div class="zh-only">{zh}</div>
  <div class="en-only">{en}</div>
</div>'''


def build_page(tool):
    global NAMES_FOR_SRC
    NAMES_FOR_SRC = NAMES[tool]
    arts = CONTENT[tool]
    body = "\n".join(render_article(a, i) for i, a in enumerate(arts, 1))
    article = "<article>\n" + body + "\n</article>"
    path = os.path.join(SITE, tool + ".html")
    text = io.open(path, encoding="utf-8").read()
    text, n = re.subn(r"<article>.*?</article>", lambda m: article, text, count=1, flags=re.S)
    if n != 1:
        problems.append(f"{tool}: 未找到 article")
        return None
    zh_len = sum(len(plain(render_blocks(a["blocks"], "zh"))) for a in arts)
    en_words = len(re.findall(r"[A-Za-z']+", render_blocks(arts and [b for a in arts for b in a["blocks"]], "en")))
    imgs = len(set(re.findall(r'<img src="([^"]+)"', body)))
    meta = (f'  <div class="meta">\n'
            f'    <span><b>{len(arts)}</b> <span class="zh-only">篇教程</span><span class="en-only">articles</span></span>\n'
            f'    <span><b>{zh_len/10000:.1f}</b> <span class="zh-only">万字</span><span class="en-only">{en_words/1000:.1f}k words</span></span>\n'
            f'    <span><b>{imgs}</b> <span class="zh-only">张图</span><span class="en-only">images</span></span>\n'
            f'  </div>')
    text = re.sub(r'\s*<div class="meta">.*?</div>', lambda m: "\n" + meta, text, count=1, flags=re.S)
    io.open(path, "w", encoding="utf-8").write(text)
    print(f"  {tool}: {len(arts)} 篇 / {zh_len/10000:.1f} 万字 / {imgs} 图")
    return arts


def toc_html(tool, arts, style="plain"):
    items = []
    for i, a in enumerate(arts, 1):
        items.append(f'<li><a href="{tool}.html#a-{a["id"]}"><span class="tg">{i:02d}</span>'
                     f'<span class="zh-only">{a["zh"]}</span><span class="en-only">{a["en"]}</span></a></li>')
    return "".join(items)


def patch_all(arts_map):
    path = os.path.join(SITE, "all.html")
    text = io.open(path, encoding="utf-8").read()
    for tool, arts in arts_map.items():
        head = f'<h2>{NAMES[tool]} · {ZH_NAMES[tool]}'
        pat = re.compile(re.escape(head) + r'.*?</ul>', re.S)
        new = (head + f' <span class="pill"><span class="zh-only block">{len(arts)} 篇</span>'
               f'<span class="en-only">{len(arts)} articles</span></span></h2>\n'
               '<ul class="toc-list">' + toc_html(tool, arts) + "</ul>")
        text, n = pat.subn(lambda m: new, text, count=1)
        if n != 1:
            problems.append(f"all.html: {tool} 分组未替换")
    text = text.replace("共 422 篇教程（419 篇官方原文 + 3 篇 AC30 补写）",
                        "共 418 篇教程（404 篇 MyCi 知识库原文 + 14 篇 AC30 官方手册编译）")
    text = text.replace("All 422 articles (419 official plus 3 written for AC30)",
                        "All 418 articles (404 from MyCi plus 14 compiled from the AC30 help)")
    io.open(path, "w", encoding="utf-8").write(text)


def patch_index(arts_map):
    path = os.path.join(SITE, "index.html")
    text = io.open(path, encoding="utf-8").read()
    for tool, arts in arts_map.items():
        head = f'<h2>{NAMES[tool]} · <span class="zh-only">{ZH_NAMES[tool]}</span>'
        pat = re.compile(re.escape(head) + r'.*?</ul>', re.S)
        new = (head + f' <span class="pill"><span class="zh-only block">{len(arts)} 篇</span>'
               f'<span class="en-only">{len(arts)} articles</span></span></h2>\n'
               '<ul class="toc-list">' + toc_html(tool, arts) + "</ul>")
        text, n = pat.subn(lambda m: new, text, count=1)
        if n != 1:
            problems.append(f"index.html: {tool} 分组未替换")
    text = text.replace('18 个工具、422 篇教程', '18 个工具、418 篇教程')
    text = text.replace('18 tools, 422 articles', '18 tools, 418 articles')
    text = text.replace('<span><b>422</b>', '<span><b>418</b>')
    text = text.replace('共 360 篇', '共 356 篇')
    io.open(path, "w", encoding="utf-8").write(text)


def patch_counts():
    for fn, pairs in {
        "about.html": [("共 422 篇教程", "共 418 篇教程"),
                       ("422 articles, 3800+ screenshots", "418 articles, 3800+ screenshots")],
        "readme.md": [("18 个工具、422 篇文章", "18 个工具、418 篇文章"),
                      ("422 篇文章，18 个工具", "418 篇文章，18 个工具")],
    }.items():
        path = os.path.join(ROOT if fn.endswith(".md") else SITE, fn)
        text = io.open(path, encoding="utf-8").read()
        for a, b in pairs:
            text = text.replace(a, b)
        io.open(path, "w", encoding="utf-8").write(text)


def main():
    arts_map = {}
    for tool in CONTENT:
        arts = build_page(tool)
        if arts:
            arts_map[tool] = arts
    patch_all(arts_map)
    patch_index(arts_map)
    patch_counts()
    print("P3b 完成；问题：", len(problems))
    for p in problems:
        print("  !", p)


NAMES_FOR_SRC = ""
if __name__ == "__main__":
    main()
