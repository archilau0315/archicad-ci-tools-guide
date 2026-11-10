#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索索引生成器

扫描站点 HTML，抽取每篇教程的中英标题，连同 18 个工具的命令路径
与中文口语关键词，输出 site/search-index.js 供 search.js 使用。

用法：
    python3 build_search_index.py [站点目录，默认 ../site]
"""
import html
import io
import json
import os
import re
import sys

# (id, 英文名, 中文名, 中文简述, 英文简述, 命令路径, 搜索关键词)
TOOLS = [
    ("annotate", "Annotate", "文字格式", "全项目文字大小写、字体批量统一",
     "Batch text case and font formatting across the whole project",
     "CI Tools → Annotate → Convert Case…",
     "大小写 转换 字体 替换 属性 文字 批量 统一 Convert Case Replace Fonts Attribute Replacement uppercase lowercase"),
    ("transformer", "Transformer", "项目镜像", "一键镜像整个项目，含 2D 标注",
     "Mirror an entire project in one click, 2D annotations included",
     "CI Tools → Transformer → Mirror Project…",
     "镜像 翻转 对称 朝向 户型 复制 Mirror Project mirror flip"),
    ("timetracker", "Time Tracker", "工时统计", "记录任务工时，与报价对比",
     "Log time per task and compare against quoted hours",
     "CI Tools → Time Tracker → Open Time Tracker",
     "工时 计时 时间 记录 报价 任务 tt Open Time Tracker timer hours"),
    ("detail", "Detail Elements", "二维详图", "拖拽式参数化详图构件库",
     "Drag-and-drop parametric 2D detail component library",
     "工具箱 → ProKit Detail Elements",
     "详图 二维 构件 图库 参数化 Detail Elements 2D library"),
    ("keynotes", "Keynotes", "规范注释", "注释数据库自动挂接与明细表",
     "Note database auto-attached by attributes, with schedules",
     "CI Tools → Keynotes → Keynotes Palette",
     "注释 标注 规范 明细表 数据库 参考键 Keynotes Palette note"),
    ("metadata", "MetaData", "属性管理", "属性与分类的批量操作面板",
     "Palette for bulk editing properties and classifications",
     "CI Tools → MetaData",
     "属性 分类 批量 数据 面板 审计 md MetaData properties classification"),
    ("quantities", "Quantities", "工程量算量", "从模型出清单，Recipe 自动分配",
     "Bill of quantities from a live model, recipes auto-assign values",
     "CI Tools → Quantities",
     "算量 工程量 清单 造价 单价 配方 表达式 qty boq Bill of Quantities Recipe CSV"),
    ("cabinets", "Cabinets", "橱柜木作", "一个对象搞定所有橱柜类型",
     "One configurable object covers every cabinet type",
     "工具箱 → ProKit Cabinets",
     "橱柜 柜体 抽屉 门板 木作 隔板 Cabinets cabinet"),
    ("doors", "Doors+Windows", "门窗", "异形门窗样式与尺寸捕捉",
     "Non-standard door and window styles with size snapping",
     "工具箱 → ProKit Doors+Windows",
     "门窗 门 窗 尺寸 捕捉 开启 样式 Doors Windows"),
    ("coverings", "Coverings", "覆面层", "墙板柱贴 3D 覆面皮",
     "3D surface skins on walls, slabs, columns and roofs",
     "工具箱 → ProKit Coverings",
     "覆面 贴皮 表皮 材质 墙 板 柱 Coverings skin"),
    ("electrical", "Electrical", "电气", "智能符号、回路与明细表",
     "Smart electrical symbols, circuits and schedules",
     "工具箱 → ProKit Electrical",
     "电气 插座 开关 灯具 回路 符号 线 elec Electrical circuit symbol"),
    ("stairs", "Stairs", "楼梯", "自由楼梯与栏杆关联",
     "Free-form stair design with associative railings",
     "工具箱 → ProKit Stairs",
     "楼梯 栏杆 踏步 平台 Stairs railing tread"),
    ("structural", "Structural", "结构构件", "桁架、框架与连接件",
     "3D structural components: trusses, frames and fixings",
     "工具箱 → ProKit Structural",
     "结构 桁架 框架 连接件 钢 梁 柱 Structural truss frame"),
    ("sites", "Sites", "场地景观", "边界、退让与植物布置",
     "Site boundaries, recession planes and plant placement",
     "工具箱 → ProKit Sites",
     "场地 边界 退让 植物 景观 总图 Sites boundary recession"),
    ("fitout", "Fitout", "室内布置", "房间一键配齐家具",
     "Furnish a room in one click from a saved set",
     "工具箱 → ProKit Fitout",
     "家具 布置 房间 室内 陈设 Fitout furnish furniture"),
    ("launchpad", "Launchpad", "启动台", "工具启动面板与常用命令入口",
     "Launcher panel for all CI Tools commands",
     "CI Tools → Launchpad",
     "启动 面板 入口 快捷 命令 Launchpad launcher"),
    ("bracing", "Bracing", "支撑（NZ）", "NZ 木结构抗侧力构件",
     "NZ timber bracing elements",
     "工具箱 → ProKit Bracing",
     "支撑 抗侧 木结构 新西兰 Bracing NZ timber"),
    ("labeller", "Labeller", "表面标注", "表面材料标注与标签",
     "Surface labelling and tags",
     "工具箱 → ProKit Labeller",
     "表面 标注 标签 材料 面层 Labeller label tag"),
]

PAGES = [
    ("index.html", "Overview", "总览与快速开始",
     "三步启动、工具卡片与全量目录", "Start here: three steps, tool cards, full index",
     "首页 总览 快速开始 三步启动 work environment library"),
    ("all.html", "All Articles", "全量文章索引",
     "按工具分册列出全部教程", "Every article, listed by tool",
     "全量 索引 目录 所有文章 all articles index"),
    ("guide.html", "Quick Guide", "中文主线速查",
     "16 个工具的操作要点", "One-page essentials for every tool",
     "速查 主线 要点 快速 guide cheat sheet"),
    ("gettingstarted.html", "Getting Started", "入门与安装",
     "安装、工作环境与图库包", "Install, work environment and library packs",
     "入门 安装 库包 工作环境 setup install libpack"),
    ("about.html", "Sources", "来源与说明",
     "内容来源与版权说明", "Sources and credits",
     "来源 说明 版权 about sources"),
]

ART_RE = re.compile(r'<div class="art" id="a-([\w.\-]+)">(.*?)(?=<div class="art" id="a-|</article>)', re.S)
ZH_RE = re.compile(r'<h3 class="zh-only block">(.*?)</h3>', re.S)
EN_RE = re.compile(r'<h3 class="en-only block">(.*?)</h3>', re.S)
TAG_RE = re.compile(r'<[^>]+>')


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(TAG_RE.sub('', s or ''))).strip()


def build(site_dir):
    site_dir = os.path.abspath(site_dir)
    labels = {t[0]: (t[1], t[2]) for t in TOOLS}
    labels["gettingstarted"] = ("Getting Started", "入门与安装")

    tools = [{
        "id": t[0], "file": t[0] + ".html", "en": t[1], "zh": t[2],
        "desc_zh": t[3], "desc_en": t[4], "cmd": t[5], "keys": t[6],
    } for t in TOOLS]

    pages = [{
        "file": p[0], "en": p[1], "zh": p[2],
        "sub_zh": p[3], "sub_en": p[4], "keys": p[5],
    } for p in PAGES]

    articles = []
    for fn in sorted(os.listdir(site_dir)):
        if not fn.endswith(".html"):
            continue
        stem = fn[:-5]
        if stem not in labels:
            continue
        text = io.open(os.path.join(site_dir, fn), encoding="utf-8").read()
        ten, tzh = labels[stem]
        for m in ART_RE.finditer(text):
            aid, block = m.group(1), m.group(2)
            mz, me = ZH_RE.search(block), EN_RE.search(block)
            zh, en = plain(mz.group(1)) if mz else "", plain(me.group(1)) if me else ""
            if not zh and not en:
                continue
            articles.append({
                "f": fn, "a": "a-" + aid, "t": stem,
                "zh": zh or en, "en": en or zh,
                "tzh": tzh, "ten": ten,
            })

    data = {
        "generated": "2026-11-10",
        "tools": tools,
        "pages": pages,
        "articles": articles,
    }
    out = os.path.join(site_dir, "search-index.js")
    io.open(out, "w", encoding="utf-8").write(
        "/* 自动生成：source/build_search_index.py —— 请勿手改 */\n"
        "window.CI_SEARCH_INDEX = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print(f"  搜索索引: {len(tools)} 个工具 / {len(pages)} 个页面 / {len(articles)} 篇文章 "
          f"→ {os.path.relpath(out, site_dir)} ({os.path.getsize(out)//1024} KB)")
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "site"))
