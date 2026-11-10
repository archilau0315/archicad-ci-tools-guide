# -*- coding: utf-8 -*-
"""建 4 个新分册页并同步全站计数。

输入：tools/rest_guide/articles.json
输出：site/{gettingstarted,launchpad,bracing,labeller}.html
      更新 site/*.html 侧栏与 hero、index 卡片、all 分组、about、readme

重复运行安全。
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "site")
DATA = json.load(open(os.path.join(HERE, "rest_guide", "articles.json"), encoding="utf-8"))
BOOKS = DATA["books"]
ARTS = DATA["articles"]

TOTAL_N = 422
TOTAL_IMG = 1330
TOTAL_WAN = 49.1

# 分册页面元信息（icon、h1、描述、en 标题）
PAGE_META = {
    "Getting Started": dict(
        icon="◎", h1_zh="入门与安装", en="Getting Started",
        desc_zh="下载、安装、激活、订阅、BIMcloud 部署与库加载",
        desc_en="Download, install, activate, subscribe, deploy to BIMcloud, and load libraries",
        title="Getting Started · 入门与安装 · CI Tools 完全指南",
        meta="Getting Started（入门与安装）完全中文教程：Ci Tools 下载安装、激活试用、订阅管理、BIMcloud 部署与库加载",
    ),
    "LaunchPad": dict(
        icon="⇪", h1_zh="启动台", en="Launchpad",
        desc_zh="项目库迁移：从 27 整体库迁到 Global Libraries",
        desc_en="Migrate project libraries from v27 monolith to Global Libraries",
        title="Launchpad · 启动台 · CI Tools 完全指南",
        meta="Launchpad（启动台）中文教程：把项目库从 Archicad 27 迁移到 Global Libraries",
    ),
    "Bracing": dict(
        icon="⊻", h1_zh="支撑（NZ 专用）", en="Bracing",
        desc_zh="按 NZS 3604 为木框架建筑自动布置支撑并生成统计表（仅新西兰）",
        desc_en="Automate NZS 3604 bracing layout and tables for timber-framed buildings (NZ only)",
        title="Bracing · 支撑（NZ 专用）· CI Tools 完全指南",
        meta="Cadimage Bracing（支撑）中文教程：按 NZS 3604 布置支撑线、支撑与支撑统计表，新西兰专用",
    ),
    "Labeller": dict(
        icon="◫", h1_zh="表面标注", en="Labeller",
        desc_zh="一键标注表面名称与面积，立面平面通用",
        desc_en="Label surface names and areas in one click, in plan or elevation",
        title="Labeller · 表面标注 · CI Tools 完全指南",
        meta="Labeller（表面标注）中文教程：在平面与立面中标注 Surface 名称、颜色与面积",
    ),
}

NEW_SIDEBAR_TOOLS = (
    '<a class="" href="launchpad.html"><span class="ic">⇪</span><span class="zh-only">Launchpad · 启动台</span><span class="en-only">Launchpad</span></a>\n'
    '<a class="" href="bracing.html"><span class="ic">⊻</span><span class="zh-only">Bracing · 支撑（NZ）</span><span class="en-only">Bracing</span></a>\n'
    '<a class="" href="labeller.html"><span class="ic">◫</span><span class="zh-only">Labeller · 表面标注</span><span class="en-only">Labeller</span></a>\n'
)
GS_SIDEBAR_LINK = (
    '<a class="" href="gettingstarted.html"><span class="ic">◎</span>'
    '<span class="zh-only">入门与安装</span><span class="en-only">Getting Started</span></a>\n'
)
FITOUT_LINK = '<a class="" href="fitout.html"><span class="ic">⌸</span><span class="zh-only">Fitout · 室内布置</span><span class="en-only">Fitout</span></a>\n'
GUIDE_LINK = '<a class="" href="guide.html"><span class="ic">★</span><span class="zh-only">中文主线速查</span><span class="en-only">Quick Guide</span></a>\n'


def art_block(a, nn):
    return (
        f'<div class="art" id="a-{a["id"]}">\n'
        f'  <div class="art-h"><span class="no">{nn:02d}</span>\n'
        f'    <h3 class="zh-only block">{a["title_zh"]}</h3>\n'
        f'    <h3 class="en-only block">{a["title_en"]}</h3>\n'
        f'  </div>\n'
        f'  <div class="art-src"><a href="{a["url"]}" target="_blank" rel="noopener">MyCi 官方原文 ↗</a></div>\n'
        f'  <div class="zh-only">{a["zh"]}</div>\n'
        f'  <div class="en-only">{a["en"]}</div>\n'
        f'  <details class="orig-toggle">\n'
        f'    <summary><span class="zh-only">英文原文对照</span><span class="en-only">Official English Original</span></summary>\n'
        f'    <div class="orig-body">\n'
        f'      <div class="orig-label"><span class="zh-only">官方英文原文</span><span class="en-only">Official English Original</span></div>\n'
        f'      {a["en"]}\n'
        f'    </div>\n'
        f'  </details>\n'
        f'</div>\n'
    )


def toc_block(cat, page):
    arts = [a for a in ARTS if a["cat"] == cat]
    lis = "".join(
        f'<li><a href="{page}#a-{a["id"]}"><span class="tg">{i + 1:02d}</span>'
        f'<span class="zh-only">{a["title_zh"]}</span>'
        f'<span class="en-only">{a["title_en"]}</span></a></li>'
        for i, a in enumerate(arts)
    )
    return f'<ul class="toc-list">{lis}</ul>\n'


def art_stats(cat):
    arts = [a for a in ARTS if a["cat"] == cat]
    n = len(arts)
    imgs = set()
    for a in arts:
        imgs.update(re.findall(r'src="(img/[^"]+)"', a["zh"]))
    ch = sum(a["n_chars"] for a in arts)
    return n, round(ch / 10000, 1), len(imgs)


def update_sidebar(html, current=None):
    # nav-h 16 -> 18
    html = html.replace(
        '<div class="nav-h zh-only block">16 个工具</div><div class="nav-h en-only block">16 Tools</div>',
        '<div class="nav-h zh-only block">18 个工具</div><div class="nav-h en-only block">18 Tools</div>')
    # fitout 后加 3 个工具链接（兼容 fitout 页自身的 on 形态）
    if NEW_SIDEBAR_TOOLS.split("\n")[0] not in html:
        fitout_on = FITOUT_LINK.replace('<a class=""', '<a class=" on"')
        if fitout_on in html:
            html = html.replace(fitout_on, fitout_on + NEW_SIDEBAR_TOOLS)
        else:
            html = html.replace(FITOUT_LINK, FITOUT_LINK + NEW_SIDEBAR_TOOLS)
    # guide 链接后加 gettingstarted
    if 'href="gettingstarted.html"' not in html:
        html = html.replace(GUIDE_LINK, GUIDE_LINK + GS_SIDEBAR_LINK)
    return html


def build_book(cat):
    meta = PAGE_META[cat]
    page = BOOKS[cat]["page"]
    n, wan, img = art_stats(cat)

    tpl = open(os.path.join(SITE, "timetracker.html"), encoding="utf-8").read()
    # sidebar：更新并去掉模板的 on，加当前页 on
    tpl = update_sidebar(tpl)
    tpl = tpl.replace('<a class=" on" href="timetracker.html"', '<a class="" href="timetracker.html"')
    cur = f'<a class="" href="{page}">'
    tpl = tpl.replace(cur, f'<a class=" on" href="{page}">', 1)

    # 内联小图标样式（27px 平台图标不被全局 img 样式拉成独占一行）
    if ".art img.inl" not in tpl:
        tpl = tpl.replace(
            "</style>",
            ".art img.inl{display:inline-block;vertical-align:-0.35em;margin:0 3px;"
            "max-width:1.7em;max-height:1.7em;border-radius:3px;box-shadow:none}\n</style>", 1)

    # head
    tpl = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{meta["meta"]}">', tpl)
    tpl = re.sub(r"<title>.*?</title>", f"<title>{meta['title']}</title>", tpl)

    # crumb + hero
    tpl = re.sub(
        r'<div class="crumb">.*?</div>',
        f'<div class="crumb"><a href="index.html"><span class="zh-only">总览</span><span class="en-only">Overview</span></a>\n'
        f'  / <span class="zh-only">{meta["en"]} · {meta["h1_zh"]}</span><span class="en-only">{meta["en"]}</span></div>',
        tpl, flags=re.S)
    kicker = "入门指南" if cat == "Getting Started" else "工具分册"
    kicker_en = "Getting Started" if cat == "Getting Started" else "Reference Chapter"
    tpl = re.sub(
        r'<div class="hero">.*?</div>\s*</div>\s*<article>',
        f'''<div class="hero">
  <span class="kicker"><span class="zh-only">{kicker}</span><span class="en-only">{kicker_en}</span></span>
  <h1>{meta["en"]} · <span class="zh-only">{meta["h1_zh"]}</span></h1>
  <p class="zh-only">{meta["desc_zh"]}</p>
  <p class="en-only">{meta["desc_en"]}</p>
  <div class="meta">
    <span><b>{n}</b> <span class="zh-only">篇教程</span><span class="en-only">articles</span></span>
    <span><b>{wan}</b> <span class="zh-only">万字</span><span class="en-only">10k words</span></span>
    <span><b>{img}</b> <span class="zh-only">张图</span><span class="en-only">images</span></span>
  </div>
</div>
<article>
<h2>{meta["en"]} · <span class="zh-only">{meta["h1_zh"]}</span></h2>
{toc_block(cat, page)}
''',
        tpl, flags=re.S)

    # article 内容（切片拼接，保住 hero 替换时插入的 h2+toc，避免 re.sub 转义）
    arts = [a for a in ARTS if a["cat"] == cat]
    body = "".join(art_block(a, i + 1) for i, a in enumerate(arts))
    i0 = tpl.index('<div class="art" id="a-')
    i1 = tpl.rindex("</article>")
    tpl = tpl[:i0] + body + "</article>" + tpl[i1 + len("</article>"):]

    open(os.path.join(SITE, page), "w", encoding="utf-8").write(tpl)
    print(f"[新页] {page}  {n} 篇 / {img} 图 / {wan} 万字")


def update_existing():
    for fn in os.listdir(SITE):
        if not fn.endswith(".html") or fn in ("gettingstarted.html", "launchpad.html", "bracing.html", "labeller.html"):
            continue
        p = os.path.join(SITE, fn)
        h = open(p, encoding="utf-8").read()
        orig = h
        h = update_sidebar(h)
        if h != orig:
            open(p, "w", encoding="utf-8").write(h)
            print(f"[侧栏] {fn}")


def update_index():
    p = os.path.join(SITE, "index.html")
    h = open(p, encoding="utf-8").read()
    # hero 计数
    h = h.replace("<b>382</b>", f"<b>{TOTAL_N}</b>")
    h = h.replace("<b>1227</b>", f"<b>{TOTAL_IMG}</b>")
    h = h.replace("<b>46.4</b>", f"<b>{TOTAL_WAN}</b>")
    h = h.replace("<b>16</b> <span", f"<b>18</b> <span")
    # 描述（修正上次漏改的旧数字）
    h = h.replace("357 篇官方文档 + 3 篇 AC30 补写、1214 张界面截图、42.5 万字，覆盖 16 个工具",
                  "419 篇官方文档 + 3 篇 AC30 补写、1330 张界面截图、49.1 万字，覆盖 18 个工具")
    h = h.replace("357 official articles plus 3 for AC30, 1214 interface screenshots, covering every feature across all 16 tools",
                  "419 official articles plus 3 for AC30, 1330 interface screenshots, covering every feature across all 18 tools")
    # meta description
    h = h.replace("16 个工具、382 篇文档、1227 张界面截图", "18 个工具、422 篇文档、1330 张界面截图")
    # h2 与卡片
    h = h.replace("<h2>16 个工具</h2>", "<h2>开始使用</h2>\n<div class=\"grid\">\n"
                  '<div class="card"><a href="gettingstarted.html">\n'
                  '  <div class="card-h"><span class="ic">◎</span><b>Getting Started</b><span class="zh-only">入门与安装</span></div>\n'
                  '  <p class="zh-only">下载、安装、激活、订阅、BIMcloud 部署与库加载</p>\n'
                  '  <p class="en-only">Download, install, activate, subscribe, deploy to BIMcloud, and load libraries</p>\n'
                  '  <div class="n"><span class="zh-only">27 篇 · 55 图</span><span class="en-only">27 articles · 55 images</span></div>\n'
                  "</a></div>\n"
                  "</div>\n\n<h2>18 个工具</h2>")
    # 工具卡（fitout 卡后追加 3 张）
    fitout_card = '</a></div>'
    # 定位 fitout 卡结尾：用其 n 行特征
    import re as _re
    m = _re.search(r'<div class="card"><a href="fitout\.html">.*?</a></div>', h, _re.S)
    if m and 'href="bracing.html"' not in h:
        cards = (
            '<div class="card"><a href="launchpad.html">\n'
            '  <div class="card-h"><span class="ic">⇪</span><b>Launchpad</b><span class="zh-only">启动台</span></div>\n'
            '  <p class="zh-only">项目库从 27 整体库迁移到 Global Libraries</p>\n'
            '  <p class="en-only">Migrate project libraries from v27 monolith to Global Libraries</p>\n'
            '  <div class="n"><span class="zh-only">2 篇 · 4 图</span><span class="en-only">2 articles · 4 images</span></div>\n'
            "</a></div>\n"
            '<div class="card"><a href="bracing.html">\n'
            '  <div class="card-h"><span class="ic">⊻</span><b>Bracing</b><span class="zh-only">支撑（NZ）</span></div>\n'
            '  <p class="zh-only">按 NZS 3604 自动布置支撑并生成统计表</p>\n'
            '  <p class="en-only">Automate NZS 3604 bracing layout and tables</p>\n'
            '  <div class="n"><span class="zh-only">10 篇 · 31 图</span><span class="en-only">10 articles · 31 images</span></div>\n'
            "</a></div>\n"
            '<div class="card"><a href="labeller.html">\n'
            '  <div class="card-h"><span class="ic">◫</span><b>Labeller</b><span class="zh-only">表面标注</span></div>\n'
            '  <p class="zh-only">一键标注表面名称与面积，立面平面通用</p>\n'
            '  <p class="en-only">Label surface names and areas in one click</p>\n'
            '  <div class="n"><span class="zh-only">1 篇 · 7 图</span><span class="en-only">1 article · 7 images</span></div>\n'
            "</a></div>\n"
        )
        h = h[:m.end()] + "\n" + cards + h[m.end():]
    open(p, "w", encoding="utf-8").write(h)
    print("[更新] index.html")


def update_all():
    p = os.path.join(SITE, "all.html")
    h = open(p, encoding="utf-8").read()
    h = h.replace("共 382 篇教程（379 篇官方原文 + 3 篇 AC30 补写），按工具分册列出。",
                  "共 422 篇教程（419 篇官方原文 + 3 篇 AC30 补写），按工具分册列出。")
    h = h.replace("All 382 articles (379 official plus 3 written for AC30), listed by tool.",
                  "All 422 articles (419 official plus 3 written for AC30), listed by tool.")
    if 'href="bracing.html"' not in h:
        groups = []
        for cat in ("Getting Started", "LaunchPad", "Bracing", "Labeller"):
            meta = PAGE_META[cat]
            page = BOOKS[cat]["page"]
            arts = [a for a in ARTS if a["cat"] == cat]
            lis = "".join(
                f'<li><a href="{page}#a-{a["id"]}"><span class="tg">{i + 1:02d}</span>'
                f'<span class="zh-only">{a["title_zh"]}</span>'
                f'<span class="en-only">{a["title_en"]}</span></a></li>'
                for i, a in enumerate(arts))
            groups.append(
                f'<h2>{meta["en"]} · <span class="zh-only">{meta["h1_zh"]}</span> <span class="pill">{len(arts)} 篇</span></h2>\n'
                f'<ul class="toc-list">{lis}</ul>')
        m = re.search(r'<h2>Fitout · 室内布置 <span class="pill">5 篇</span></h2>\s*<ul class="toc-list">.*?</ul>', h, re.S)
        h = h[:m.end()] + "\n" + "\n".join(groups) + h[m.end():]
    open(p, "w", encoding="utf-8").write(h)
    print("[更新] all.html")


def update_about():
    p = os.path.join(SITE, "about.html")
    h = open(p, encoding="utf-8").read()
    h = h.replace("共 379 篇官方文档、1227 张界面截图", "共 419 篇官方文档、1330 张界面截图")
    h = h.replace("357 篇全文翻译", "419 篇全文翻译")
    open(p, "w", encoding="utf-8").write(h)
    print("[更新] about.html")


def update_guide():
    p = os.path.join(SITE, "guide.html")
    h = open(p, encoding="utf-8").read()
    h = h.replace("16 个工具中文主线速查", "18 个工具中文主线速查")
    h = h.replace("16 个工具操作要点", "18 个工具操作要点")
    h = h.replace("covering all 16 tools", "covering all 18 tools")
    open(p, "w", encoding="utf-8").write(h)
    print("[更新] guide.html")


def update_readme():
    p = os.path.join(HERE, "..", "readme.md")
    h = open(p, encoding="utf-8").read()
    h = h.replace("articles-382", f"articles-{TOTAL_N}").replace("screenshots-1227", f"screenshots-{TOTAL_IMG}")
    h = h.replace("379 篇官方文档全部译为中文、1227 张界面截图", "419 篇官方文档全部译为中文、1330 张界面截图")
    h = h.replace("按 16 个工具分册整理", "按 18 个工具与入门分册整理")
    open(p, "w", encoding="utf-8").write(h)
    print("[更新] readme.md")


def main():
    for cat in ("Getting Started", "LaunchPad", "Bracing", "Labeller"):
        build_book(cat)
    update_existing()
    update_index()
    update_all()
    update_about()
    update_guide()
    update_readme()
    print("全部完成")


if __name__ == "__main__":
    main()
