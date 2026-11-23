#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按工具页实际文章同步 index/all 目录与全站计数。"""
import io
import os
import re

from build_search_index import TOOLS
from rebrand_prokit import toc_section

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SITE = os.path.join(ROOT, "site")
ALIASES = {
    "metadata": ("Metadata", "MetaData"),
    "doors": ("Doors + Windows", "Doors+Windows"),
    "structural": ("Structure", "Structural"),
    "sites": ("Site", "Sites"),
    "launchpad": ("LaunchPad", "Launchpad"),
}


def read(name, root=SITE):
    return io.open(os.path.join(root, name), encoding="utf-8").read()


def write(name, text, root=SITE):
    io.open(os.path.join(root, name), "w", encoding="utf-8").write(text)


def section(tool, en, zh, index_style):
    title = f"{en} · " + (f'<span class="zh-only">{zh}</span>' if index_style else zh)
    block = toc_section(tool, title).strip()
    if index_style:
        block = re.sub(
            r'<span class="pill">(\d+) 篇</span>',
            r'<span class="pill"><span class="zh-only block">\1 篇</span>'
            r'<span class="en-only">\1 articles</span></span>', block)
    return block


def sync_groups(text, index_style):
    missing = []
    for tool, en, zh, *_ in TOOLS:
        block = section(tool, en, zh, index_style)
        names = ALIASES.get(tool, (en,))
        pattern = re.compile(r"<h2>(?:" + "|".join(map(re.escape, names)) + r") · .*?</ul>", re.S)
        text, count = pattern.subn(lambda _: block, text, count=1)
        if not count:
            missing.append(block)
    if missing:
        if not index_style or len(missing) != 3:
            raise RuntimeError(f"目录缺少非预期分组：{len(missing)} 个")
        text = text.replace('<footer class="foot">', "\n".join(missing) + '\n<footer class="foot">', 1)
    return text


def sync_index():
    text = sync_groups(read("index.html"), True)
    text = text.replace("18 个工具、418 篇教程", "18 个工具、424 篇教程")
    text = text.replace("18 tools, 418 articles", "18 tools, 424 articles")
    text = text.replace("<span><b>418</b>", "<span><b>424</b>", 1)
    text = text.replace("共 356 篇，点标题直达对应分册的具体文章。",
                        "共 391 篇，点标题直达对应分册的具体文章。")
    text = text.replace("下载、安装、激活、订阅、BIMcloud 部署与库加载",
                        "ProKit 两包授权、下载、安装、自检与版本兼容；附旧版安装归档")
    text = text.replace("Download, install, activate, subscribe, deploy to BIMcloud, and load libraries",
                        "ProKit eligibility, installers, setup checks and compatibility, plus the legacy archive")
    text = re.sub(
        r'<div class="n"><span class="zh-only">27 篇 · 56 图</span>'
        r'<span class="en-only">27 articles · 56 images</span></div>',
        '<div class="n"><span class="zh-only">33 篇 · 6 主线 + 27 归档</span>'
        '<span class="en-only">33 articles · 6 AC30 + 27 legacy</span></div>', text, count=1)
    write("index.html", text)


def sync_all():
    text = sync_groups(read("all.html"), False)
    text = re.sub(
        r"共 418 篇教程（404 篇 MyCi 知识库原文 \+ 14 篇 AC30 官方手册编译），按工具分册列出。",
        "共 391 篇工具教程（377 篇 MyCi 知识库原文 + 14 篇 AC30 官方手册编译），按工具分册列出；入门与安装另有 33 篇。", text, count=1)
    text = re.sub(
        r"All 418 articles \(404 from MyCi plus 14 compiled from the AC30 help\), listed by tool\.",
        "All 391 tool articles (377 from MyCi plus 14 compiled from the AC30 help), listed by tool; Getting Started has another 33 articles.", text, count=1)
    write("all.html", text)


def sync_totals():
    about = read("about.html").replace("共 418 篇教程", "共 424 篇教程").replace(
        "418 articles, 3800+ screenshots", "424 articles, 3800+ screenshots")
    write("about.html", about)
    readme = read("readme.md", ROOT).replace("articles-418-", "articles-424-")
    readme = readme.replace("18 个工具、418 篇文章", "18 个工具、424 篇文章")
    readme = readme.replace("418 篇文章，18 个工具 + 入门", "424 篇文章，18 个工具 + 入门")
    write("readme.md", readme, ROOT)


def main():
    expected = sum(len(re.findall(r'<div class="art" id="a-', read(t[0] + ".html"))) for t in TOOLS)
    getting_started = len(re.findall(r'<div class="art" id="a-', read("gettingstarted.html")))
    if (expected, getting_started) != (391, 33):
        raise RuntimeError(f"计数不符：工具 {expected}，入门 {getting_started}；预期 391 / 33")
    sync_index()
    sync_all()
    sync_totals()
    print(f"目录与计数已同步：工具 {expected} + 入门 {getting_started} = 全站 {expected + getting_started}")


if __name__ == "__main__":
    main()
