#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ProKit 外壳批量改造（P4）

只改外壳，不动正文：
  1. 品牌名 / <title> / 页脚 → ProKit / CI Tools（旧）
  2. 侧栏导航改为三组（ProKit Core / ProKit Suite / 旧版）
  3. 工具页 hero 加包徽标 + 官方入口链接
  4. 命令路径 CI Tools > X → ProKit > X（历史语境行跳过）
  5. guide.html / all.html 同步改名

用法：
    python source/rebrand_prokit.py --dry-run
    python source/rebrand_prokit.py
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))
REPORT = os.path.abspath(os.path.join(HERE, "..", "docs", "rebrand_report.md"))

OFFICIAL = "https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/"
MYCI = "https://cadimage.zendesk.com/hc/en-us"

# id, 英文名, 中文名, 图标, 包, 官方链接
TOOLS = [
    ("annotate", "Annotate", "文字格式", "Aa", "core", OFFICIAL + "Annotate/AnnotateIntro.html"),
    ("transformer", "Transformer", "项目镜像", "⇄", "core", OFFICIAL + "Transformer/Transformer_Intro.html"),
    ("timetracker", "Time Tracker", "工时统计", "◷", "core", OFFICIAL + "TimeTracker/Tracker_HowTo.html"),
    ("detail", "Detail Elements", "二维详图", "▤", "core", OFFICIAL + "DetailElements/DetailAddTool.html"),
    ("keynotes", "Keynotes", "规范注释", "❝", "suite", MYCI),
    ("metadata", "Metadata", "属性管理", "◈", "suite", MYCI),
    ("quantities", "Quantities", "工程量算量", "∑", "suite", MYCI),
    ("cabinets", "Cabinets", "橱柜木作", "▦", "suite", MYCI),
    ("doors", "Doors + Windows", "门窗", "⌸", "suite", MYCI),
    ("coverings", "Coverings", "覆面层", "▨", "suite", MYCI),
    ("electrical", "Electrical", "电气", "⚡", "suite", MYCI),
    ("stairs", "Stairs", "楼梯", "⇱", "suite", MYCI),
    ("structural", "Structure", "结构构件", "⌗", "suite", MYCI),
    ("sites", "Site", "场地景观", "⛿", "suite", MYCI),
    ("fitout", "Fitout", "室内布置", "⌸", "suite", MYCI),
    ("launchpad", "LaunchPad", "启动台", "⇪", "old", MYCI),
    ("bracing", "Bracing", "支撑（NZ）", "⊻", "old", MYCI),
    ("labeller", "Labeller", "表面标注", "◫", "old",
     "https://centralinnovation.com/resources/use-the-new-ci-tools-labeller-to-label-surfaces-with-ease"),
]
T = {t[0]: t for t in TOOLS}

PKG_LABEL = {"core": "ProKit Core", "suite": "ProKit Suite", "old": "旧版工具"}
PKG_NOTE = {
    "core": ("AC30 官方手册已覆盖", "Covered by the AC30 official manual"),
    "suite": ("随 Archicad Collaborate / Max 提供", "Included with Archicad Collaborate / Max"),
    "old": ("未纳入 ProKit 两个安装包", "Not part of either ProKit installer"),
}
PKG_LINK = {
    "core": ("Graphisoft AC30 帮助 ↗", "Graphisoft AC30 help ↗"),
    "suite": ("MyCi 知识库 ↗", "MyCi knowledge base ↗"),
    "old": ("参阅官方说明 ↗", "Official note ↗"),
}

OLD_BRAND = ('<div class="brand"><a href="index.html"><div class="brand-t">'
             '<span class="zh-only">CI Tools 完全指南</span>'
             '<span class="en-only">CI Tools Handbook</span></div>'
             '<div class="brand-s">Archicad Plugin Manual</div></a></div>')
NEW_BRAND = ('<div class="brand"><a href="index.html"><div class="brand-t">'
             '<span class="zh-only">ProKit / CI Tools（旧）</span>'
             '<span class="en-only">ProKit / CI Tools (legacy)</span></div>'
             '<div class="brand-s">Archicad ProKit · AC30</div></a></div>')
TITLE_RE = re.compile(r'·\s*CI Tools 完全指南</title>')
NEW_TITLE = " · ProKit / CI Tools（旧）</title>"
OLD_FOOT_ZH = ('<span class="zh-only">CI Tools 完全指南 · 内容整理自 Central Innovation / '
               'Graphisoft 官方 MyCi 知识库（2026-10 更新）· 2026-11-05</span>')
NEW_FOOT_ZH = ('<span class="zh-only">ProKit / CI Tools（旧） · 内容依据 Graphisoft AC30 官方帮助与 '
               'MyCi 知识库 · 2026-11-23</span>')
OLD_FOOT_EN = ('<span class="en-only">CI Tools Handbook · Content from the official Central '
               'Innovation / Graphisoft MyCi knowledge base (updated 2026-10) · 2026-11-05</span>')
NEW_FOOT_EN = ('<span class="en-only">ProKit / CI Tools (legacy) · Sources: Graphisoft AC30 help '
               'and the MyCi knowledge base · 2026-11-23</span>')

MARK = "<!-- rebrand:prokit-p4 -->"
CSS = """
/* ProKit 包徽标（P4） */
.pkg-line{margin:12px 0 0;font-size:12.5px;color:var(--muted);display:flex;
  flex-wrap:wrap;gap:8px;align-items:center}
.pkg-line a{border:none;font-size:12.5px}
.pkg{display:inline-block;font-size:10.5px;font-weight:600;letter-spacing:.03em;
  padding:2px 8px;border-radius:9999px;white-space:nowrap}
.pkg-core{background:rgba(47,111,143,.12);color:#1d4d63;border:1px solid rgba(47,111,143,.25)}
.pkg-suite{background:#f1e7d8;color:#8a5a1e;border:1px solid #e2d2ba}
.pkg-old{background:#f7e3e3;color:#9a3b3b;border:1px solid #e6c6c6}
"""

START_NAV = [
    ("index.html", "◈", "总览与快速开始", "Overview"),
    ("all.html", "☰", "全量文章索引", "All Articles"),
    ("guide.html", "★", "中文主线速查", "Quick Guide"),
    ("differences.html", "⇋", "ProKit 与 CI Tools", "ProKit vs CI Tools"),
    ("gettingstarted.html", "◎", "入门与安装", "Getting Started"),
]
GROUPS = [
    ("core", "ProKit Core · 4", "ProKit Core · 4"),
    ("suite", "ProKit Suite · 11", "ProKit Suite · 11"),
    ("old", "其他 / 旧版 · 3", "Legacy · 3"),
]
OLD_LEGACY_NAV = ('<div class="nav-h zh-only block">其他 / 旧版 · 3</div>'
                  '<div class="nav-h en-only block">其他 / 旧版 · 3</div>')
NEW_LEGACY_NAV = ('<div class="nav-h zh-only block">其他 / 旧版 · 3</div>'
                  '<div class="nav-h en-only block">Legacy · 3</div>')
LEGACY_EN = {"launchpad": "LaunchPad", "bracing": "Bracing", "labeller": "Labeller"}


def nav_link(current, href, icon, zh, en):
    cls = ' class="on"' if current == href else ' class=""'
    return (f'<a{cls} href="{href}"><span class="ic">{icon}</span>'
            f'<span class="zh-only">{zh}</span><span class="en-only">{en}</span></a>')


def build_nav(current):
    out = ['<div class="nav-h zh-only block">开始</div>'
           '<div class="nav-h en-only block">Start</div>']
    for href, icon, zh, en in START_NAV:
        out.append(nav_link(current, href, icon, zh, en))
    for pkg, zh_title, en_title in GROUPS:
        out.append(f'<div class="nav-h zh-only block">{zh_title}</div>'
                   f'<div class="nav-h en-only block">{en_title}</div>')
        for tid, en, zh, icon, p, _ in TOOLS:
            if p != pkg:
                continue
            if tid == "doors":
                en = "Doors + Windows"
            out.append(nav_link(current, tid + ".html", icon, f"{en} · {zh}", en))
    return "\n".join(out) + "\n"


def badge(tid):
    _, en, zh, _, pkg, src = T[tid]
    nzh, nen = PKG_NOTE[pkg]
    lzh, len_ = PKG_LINK[pkg]
    return (f'  <p class="pkg-line"><span class="pkg pkg-{pkg}">{PKG_LABEL[pkg]}</span>'
            f'<span class="zh-only">{nzh} · </span><span class="en-only">{nen} · </span>'
            f'<a href="{src}" target="_blank" rel="noopener">'
            f'<span class="zh-only">{lzh}</span><span class="en-only">{len_}</span></a></p>')


NAV_RE = re.compile(r'<div class="nav-h zh-only block">开始</div>.*?'
                    r'(?=<div class="nav-h zh-only block">关于</div>)', re.S)
HERO_RE = re.compile(r'(<div class="hero">.*?</h1>)', re.S)

# 历史语境行：保留旧名与旧入口
WHITELIST = ("AC28", "AC29", "AC 28", "AC 29", "旧版", "老版", "MyCi", "Cadimage",
             "legacy", "Legacy", "Ci Tools Profile", "CI Tools Profile")
PATH_PATTERNS = [
    (re.compile(r'\bCI Tools\s*(?:→|>|&gt;)\s*'), "ProKit > "),
    (re.compile(r'\bCi Tools\s*(?:→|>|&gt;)\s*'), "ProKit > "),
]
PATH_FIX = [
    ("ProKit > Doors+Windows", "ProKit > Doors + Windows"),
    ("ProKit > Structural", "ProKit > Structure"),
    ("ProKit > Sites", "ProKit > Site"),
    ("ProKit > MetaData", "ProKit > Metadata"),
    ("ProKit > Launchpad", "ProKit > LaunchPad"),
]
RENAME = [
    ("Doors+Windows · 门窗", "Doors + Windows · 门窗"),
    ("Structural · 结构构件", "Structure · 结构构件"),
    ("Sites · 场地景观", "Site · 场地景观"),
    ("MetaData · 属性管理", "Metadata · 属性管理"),
    ("Launchpad · 启动台", "LaunchPad · 启动台"),
    ('class="en-only">Sites</span></div>', 'class="en-only">Site</span></div>'),
    ('class="en-only">Structural</span></div>', 'class="en-only">Structure</span></div>'),
    ('class="en-only">MetaData</span></div>', 'class="en-only">Metadata</span></div>'),
    ('class="en-only">Doors+Windows</span></div>', 'class="en-only">Doors + Windows</span></div>'),
    ('class="en-only">Launchpad</span></div>', 'class="en-only">LaunchPad</span></div>'),
]
H1_FIX = [("Doors+Windows", "Doors + Windows"), ("Structural", "Structure"),
          ("Sites", "Site"), ("MetaData", "Metadata"), ("Launchpad", "LaunchPad")]
HTML_SUFFIX = {"index.html", "all.html", "guide.html", "about.html",
               "gettingstarted.html", "differences.html"}


def fix_line(line):
    if any(w in line for w in WHITELIST):
        return line, 0
    n = 0
    for pat, rep in PATH_PATTERNS:
        line, k = pat.subn(rep, line)
        n += k
    for a, b in PATH_FIX:
        if a in line:
            n += line.count(a)
            line = line.replace(a, b)
    if "CI Tools dropdown" in line or "Ci Tools dropdown" in line:
        n += 1
        line = line.replace("CI Tools dropdown", "ProKit menu").replace(
            "Ci Tools dropdown", "ProKit menu")
    if "CI Tools 下拉菜单" in line:
        n += 1
        line = line.replace("CI Tools 下拉菜单", "ProKit 菜单")
    return line, n


def rebrand_tool(fn, text):
    tid = fn[:-5]
    stats = {"path": 0, "nav": 0, "badge": 0, "brand": 0}
    text = text.replace(OLD_BRAND, NEW_BRAND)
    if NEW_BRAND in text:
        stats["brand"] = 1
    text = TITLE_RE.sub(NEW_TITLE, text, count=1)
    text = text.replace(OLD_FOOT_ZH, NEW_FOOT_ZH).replace(OLD_FOOT_EN, NEW_FOOT_EN)
    text = text.replace(OLD_LEGACY_NAV, NEW_LEGACY_NAV)
    for a, b in RENAME:
        text = text.replace(a, b)
    for a, b in H1_FIX:
        text = re.sub(r'<h1>%s · ' % re.escape(a), f'<h1>{b} · ', text, count=1)
    # 逐行替换命令路径
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        lines[i], k = fix_line(ln)
        stats["path"] += k
    text = "\n".join(lines)
    # 导航三组化
    if "ProKit Core · 4" not in text:
        text, k = NAV_RE.subn(lambda m: build_nav(fn), text, count=1)
        stats["nav"] = k
    # hero 徽标
    if "pkg-line" not in text:
        text, k = HERO_RE.subn(lambda m: m.group(1) + "\n" + badge(tid), text, count=1)
        stats["badge"] = k
    # 样式
    if ".pkg-line{" not in text:
        text = text.replace("</style>", CSS + "</style>", 1)
    if MARK not in text:
        text = text.replace("<head>", "<head>\n" + MARK, 1)
    return text, stats


def rebrand_misc(fn, text):
    stats = {"path": 0, "nav": 0, "badge": 0, "brand": 0}
    text = text.replace(OLD_BRAND, NEW_BRAND)
    if NEW_BRAND in text:
        stats["brand"] = 1
    text = TITLE_RE.sub(NEW_TITLE, text, count=1)
    text = text.replace(OLD_FOOT_ZH, NEW_FOOT_ZH).replace(OLD_FOOT_EN, NEW_FOOT_EN)
    text = text.replace(OLD_LEGACY_NAV, NEW_LEGACY_NAV)
    text = text.replace("CI Tools 18 个工具", "ProKit 18 个工具")
    for a, b in RENAME:
        text = text.replace(a, b)
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        lines[i], k = fix_line(ln)
        stats["path"] += k
    text = "\n".join(lines)
    if "ProKit Core · 4" not in text:
        text, k = NAV_RE.subn(lambda m: build_nav(fn), text, count=1)
        stats["nav"] = k
    if ".pkg-line{" not in text:
        text = text.replace("</style>", CSS + "</style>", 1)
    if MARK not in text:
        text = text.replace("<head>", "<head>\n" + MARK, 1)
    return text, stats


def extra_guide(text):
    """guide：补 LaunchPad / Labeller 两节，并更新 16→18 表述。"""
    text = text.replace("别一次学 16 个。", "别一次学 18 个。")
    text = text.replace("CI Tools 中文主线 · 18 个工具操作要点",
                        "ProKit / CI Tools（旧）· 18 个工具操作要点")
    text = text.replace("Coverings、Doors+Windows", "Coverings、Doors + Windows")
    text = text.replace("Cabinets、Doors+Windows、Electrical", "Cabinets、Doors + Windows、Electrical")
    text = text.replace("（无中国国标库）、Structural、Bracing", "（无中国国标库）、Structure、Bracing")
    text = text.replace("<h3>三步启动（每次新项目必做）</h3>",
                        "<h3>三步启动（每次新项目必做）</h3>\n"
                        "<p>> 以下为旧版 CI Tools 的工作环境准备流程；AC30 ProKit 的安装与授权判断见 "
                        "<a href=\"gettingstarted.html\">入门与安装</a>。</p>")
    text = text.replace(
        "<p>> 适用 Archicad 24 及以上版本。</p>",
        "<p>> 适用 Archicad 24 及以上版本。AC30 起菜单品牌改为 <strong>ProKit</strong>，"
        "以下路径按 <code>ProKit &gt; 工具</code> 书写；旧版菜单仍是 <code>CI Tools &gt; 工具</code>，功能一致。</p>")
    sections = (
        "<h2>十七、LaunchPad · 启动台</h2>\n"
        "<p><strong>干什么</strong>：把 ProKit 各工具的命令收进一个启动面板，少翻菜单。</p>\n"
        "<p><strong>入口</strong>：ProKit &gt; LaunchPad</p>\n"
        "<p>> LaunchPad 未在两个 ProKit 安装包中单列，新版入口以安装后菜单为准。</p>\n"
        "<p>---</p>\n"
        "<h2>十八、Labeller · 表面标注</h2>\n"
        "<p><strong>干什么</strong>：给墙面、板面等表面自动加材料 / 做法标注，省去逐个手动标签。</p>\n"
        "<p><strong>入口</strong>：ProKit &gt; Labeller（旧版为 CI Tools &gt; Labeller）</p>\n"
        "<p>> Labeller 是免费的 CI Tools 工具，<strong>不在 ProKit Core / Suite 两个包内</strong>，"
        "MyCi 的 ProKit 分区也未收录。</p>\n"
        "<p>---</p>\n"
    )
    anchor = "<h2>学习路径建议</h2>"
    if anchor in text and "十七、LaunchPad" not in text:
        text = text.replace(anchor, sections + anchor, 1)
    # 英文目录补三条
    extra = ('<li><a href="launchpad.html"><span class="tg">⇪</span>LaunchPad — Launcher panel for ProKit commands</a></li>'
             '<li><a href="bracing.html"><span class="tg">⊻</span>Bracing — NZ timber bracing (NZ only)</a></li>'
             '<li><a href="labeller.html"><span class="tg">◫</span>Labeller — Surface labelling (free CI Tools tool)</a></li>')
    if "LaunchPad — Launcher panel" not in text:
        text = text.replace("</ul>\n<p>Tip:", extra + "</ul>\n<p>Tip:", 1)
    text = text.replace("Structural — 3D structural", "Structure — 3D structural")
    text = text.replace("Sites — Site boundaries", "Site — Site boundaries")
    text = text.replace("MetaData — Palette", "Metadata — Palette")
    text = text.replace("Doors+Windows — Non-standard", "Doors + Windows — Non-standard")
    text = text.replace("<td>Cabinets、Coverings、Doors+Windows", "<td>Cabinets、Coverings、Doors + Windows")
    text = text.replace("Keynotes、MetaData、Quantities、Site、Stairs、Structure",
                        "Keynotes、Metadata、Quantities、Site、Stairs、Structure")
    return text


ART_RE = re.compile(r'<div class="art" id="(a-[\w.\-]+)">(.*?)'
                    r'(?=<div class="art" id="a-|</article>)', re.S)
H3_ZH = re.compile(r'<h3 class="zh-only block">(.*?)</h3>', re.S)
H3_EN = re.compile(r'<h3 class="en-only block">(.*?)</h3>', re.S)


def toc_section(tid, zh_name):
    """从工具页抽取文章标题，生成 all.html 的一个分组。"""
    text = io.open(os.path.join(SITE, tid + ".html"), encoding="utf-8").read()
    items = []
    for m in ART_RE.finditer(text):
        aid, block = m.group(1), m.group(2)
        mz, me = H3_ZH.search(block), H3_EN.search(block)
        if not mz:
            continue
        zh = mz.group(1).strip()
        en = me.group(1).strip() if me else zh
        items.append(f'<li><a href="{tid}.html#{aid}"><span class="tg">{len(items)+1:02d}</span>'
                     f'<span class="zh-only">{zh}</span><span class="en-only">{en}</span></a></li>')
    return (f'\n<h2>{zh_name} <span class="pill">{len(items)} 篇</span></h2>\n'
            f'<ul class="toc-list">{"".join(items)}</ul>\n')


def extra_all(text):
    """all：分组标题按官方名统一，并补齐旧版 3 个工具。"""
    text = text.replace("MetaData · 属性管理", "Metadata · 属性管理")
    text = text.replace("Doors+Windows · 门窗", "Doors + Windows · 门窗")
    text = text.replace("Structural · 结构构件", "Structure · 结构构件")
    text = text.replace("Sites · 场地景观", "Site · 场地景观")
    if '>LaunchPad · 启动台 <span class="pill">' not in text:
        blocks = (toc_section("launchpad", "LaunchPad · 启动台")
                  + toc_section("bracing", "Bracing · 支撑（NZ）")
                  + toc_section("labeller", "Labeller · 表面标注"))
        text = text.replace('<footer class="foot">', blocks + '<footer class="foot">', 1)
    return text


def main():
    dry = "--dry-run" in sys.argv
    rows, total = [], 0
    for fn in sorted(os.listdir(SITE)):
        if not fn.endswith(".html") or fn in HTML_SUFFIX:
            continue
        path = os.path.join(SITE, fn)
        text = io.open(path, encoding="utf-8").read()
        new, st = rebrand_tool(fn, text)
        if new != text:
            total += 1
            if not dry:
                io.open(path, "w", encoding="utf-8").write(new)
            rows.append((fn, st))
    for fn, func in (("guide.html", extra_guide), ("all.html", extra_all),
                     ("about.html", lambda text: text)):
        path = os.path.join(SITE, fn)
        text = io.open(path, encoding="utf-8").read()
        new, st = rebrand_misc(fn, text)
        new = func(new)
        if new != text:
            total += 1
            if not dry:
                io.open(path, "w", encoding="utf-8").write(new)
            rows.append((fn, st))
    # 首页与差异页保留各自正文，只统一侧栏名称和分组。
    for fn in ("index.html", "differences.html"):
        path = os.path.join(SITE, fn)
        text = io.open(path, encoding="utf-8").read()
        new, n = NAV_RE.subn(lambda m: build_nav(fn), text, count=1)
        if new != text:
            total += 1
            if not dry:
                io.open(path, "w", encoding="utf-8").write(new)
            rows.append((fn, {"path": 0, "nav": n, "badge": 0, "brand": 0}))

    out = ["# ProKit 外壳改造报告（P4）", "",
           f"- 模式：{'试运行 dry-run' if dry else '已写入'}",
           f"- 改动文件：{total}", "",
           "| 文件 | 命令路径 | 导航 | 徽标 | 品牌 |", "|---|---|---|---|---|"]
    for fn, st in rows:
        out.append(f"| {fn} | {st['path']} | {st['nav']} | {st['badge']} | {st['brand']} |")
    io.open(REPORT, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"P4 {'dry-run' if dry else '完成'}：{total} 个文件，报告 {os.path.relpath(REPORT, SITE)}")


if __name__ == "__main__":
    main()
