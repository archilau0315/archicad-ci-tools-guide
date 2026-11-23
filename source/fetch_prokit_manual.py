#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取 AC30 官方 ProKit Core 帮助（P3a）

输出：
  docs/prokit_manual/<tool>/*.html      页面快照
  assets/img/prokit/<tool>/*.png        配图（本地化）
  docs/prokit_manual/manifest.json      页面 / 图片 / URL / MD5 / 日期

用法：
    python source/fetch_prokit_manual.py
"""
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.parse as up
import urllib.request as ur

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DOCS = os.path.join(ROOT, "docs", "prokit_manual")
IMGS = os.path.join(ROOT, "site", "img", "prokit")
CORE = "https://help.graphisoft.com/AC/30/INT/Topics/960_Prokit/ProKit_Core/"
SEEDS = {
    "annotate": CORE + "Annotate/AnnotateIntro.html",
    "transformer": CORE + "Transformer/Transformer_Intro.html",
    "timetracker": CORE + "TimeTracker/Tracker_HowTo.html",
    "detail": CORE + "DetailElements/DetailAddTool.html",
}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProKitManualFetcher/1.0"}
A_RE = re.compile(r'<a[^>]+href="([^"#?]+\.html)"', re.I)
IMG_RE = re.compile(r'<img[^>]+src="([^"]+)"', re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)

fails = []


def get(url, binary=False):
    req = ur.Request(url, headers=UA)
    with ur.urlopen(req, timeout=30) as r:
        return r.read() if binary else r.read().decode("utf-8", "ignore")


def md5(data):
    return hashlib.md5(data).hexdigest()


def same_dir(url, base):
    """仅接受工具同目录及其子目录的页面。"""
    folder = base.rsplit("/", 1)[0] + "/"
    return url.startswith(folder) and url.endswith(".html")


def crawl(tool, seed, max_pages=8):
    """从入口页 BFS 收集同目录页面。"""
    pages, queue, seen = [], [seed], set()
    while queue and len(pages) < max_pages:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            html = get(url)
        except Exception as e:  # 单页失败不中断
            fails.append(f"页面 {url} → {e}")
            continue
        pages.append((url, html))
        for href in A_RE.findall(html):
            nxt = up.urljoin(url, href)
            if same_dir(nxt, seed) and nxt not in seen:
                queue.append(nxt)
        time.sleep(0.2)
    return pages


def save_page(tool, url, html):
    folder = os.path.join(DOCS, tool)
    os.makedirs(folder, exist_ok=True)
    name = url.rsplit("/", 1)[1]
    path = os.path.join(folder, name)
    io.open(path, "w", encoding="utf-8").write(html)
    m = TITLE_RE.search(html)
    return {
        "local": os.path.relpath(path, ROOT).replace("\\", "/"),
        "url": url,
        "title": re.sub(r"\s+", " ", m.group(1)).strip() if m else name,
    }


def save_images(tool, page_url, html, manifest):
    folder = os.path.join(IMGS, tool)
    os.makedirs(folder, exist_ok=True)
    n = 0
    for src in IMG_RE.findall(html):
        if not re.search(r"\.(png|jpg|jpeg|gif)$", src, re.I):
            continue
        url = up.urljoin(page_url, src)
        name = re.sub(r"[^\w.\-]", "_", url.rsplit("/", 1)[1])
        path = os.path.join(folder, name)
        try:
            if os.path.exists(path):
                old = io.open(path, "rb").read()
                data = get(url, True)
                if md5(old) == md5(data):
                    n += 1
                    continue
            else:
                data = get(url, True)
                time.sleep(0.15)
            io.open(path, "wb").write(data)
            manifest.append({
                "tool": tool,
                "local": os.path.relpath(path, ROOT).replace("\\", "/"),
                "url": url,
                "md5": md5(data),
                "page": page_url,
            })
            n += 1
        except Exception as e:
            fails.append(f"图片 {url} → {e}")
    return n


def main():
    os.makedirs(DOCS, exist_ok=True)
    manifest, pages_meta = [], []
    for tool, seed in SEEDS.items():
        pages = crawl(tool, seed)
        imgs = 0
        for url, html in pages:
            pages_meta.append(dict(tool=tool, **save_page(tool, url, html)))
            imgs += save_images(tool, url, html, manifest)
        print(f"  {tool}: {len(pages)} 页 / {imgs} 图")
    out = {
        "source": "Graphisoft AC30 help · ProKit Core",
        "fetched": time.strftime("%Y-%m-%d"),
        "pages": pages_meta,
        "images": manifest,
    }
    io.open(os.path.join(DOCS, "manifest.json"), "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=2))
    print(f"汇总：{len(pages_meta)} 页 / {len(manifest)} 图；失败 {len(fails)}")
    for f in fails:
        print("  !", f)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
