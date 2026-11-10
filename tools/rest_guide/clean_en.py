# -*- coding: utf-8 -*-
"""清洗剩余 4 分册的官方 HTML：Word 导出脏样式 + YouTube iframe 转链接 + 失效图删除。

输入：tools/rest_guide/raw/{id}.json（html 字段）
输出：tools/rest_guide/en_clean/{id}.html
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "en_clean")


def iframe_to_link(m):
    tag = m.group(0)
    src = re.search(r'src="([^"]+)"', tag)
    if not src:
        return ""
    u = src.group(1)
    if u.startswith("//"):
        u = "https:" + u
    vid = re.search(r"/embed/([A-Za-z0-9_-]{6,})", u)
    if vid:
        watch = f"https://www.youtube.com/watch?v={vid.group(1)}"
    else:
        watch = u
    t = re.search(r'start=(\d+)', u)
    label = "▶ <b>观看官方视频（YouTube）</b>"
    if t:
        label += f"（从 {t.group(1)} 秒处开始）"
    return f'<p><a href="{watch}" target="_blank" rel="noopener">{label} ↗</a></p>'


def clean(html):
    # iframe -> 视频链接
    html = re.sub(r"<iframe[^>]*>(?:</iframe>)?", iframe_to_link, html, flags=re.I)
    # 删除仍指向外域的 img（官方附件已 404）
    html = re.sub(r'<img[^>]*src="(https?://[^"]+)"[^>]*>', "", html)
    # 去 script/style
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S | re.I)
    # <font> <span> 拆包装
    while re.search(r"<(font|span)\b[^>]*>", html):
        html = re.sub(r"<(font|span)\b[^>]*>(.*?)</\1>", r"\2", html, flags=re.S | re.I)
    # 去属性（img/a 保留必要属性）
    def strip_attrs(m):
        tag, attrs = m.group(1), m.group(2)
        if tag == "img":
            src = re.search(r'src="([^"]*)"', attrs)
            alt = re.search(r'alt="([^"]*)"', attrs)
            return f'<img src="{src.group(1) if src else ""}" alt="{alt.group(1) if alt else ""}" loading="lazy">'
        if tag == "a":
            href = re.search(r'href="([^"]*)"', attrs)
            return f'<a href="{href.group(1) if href else "#"}" target="_blank" rel="noopener">'
        return f"<{tag}>"
    html = re.sub(r"<([a-zA-Z0-9]+)((?:\s+[^>]*?)?)>", strip_attrs, html)
    html = re.sub(r"<p>\s*</p>", "", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for fn in sorted(os.listdir(RAW)):
        if not fn.endswith(".json"):
            continue
        d = json.load(io.open(os.path.join(RAW, fn), encoding="utf-8"))
        io.open(os.path.join(OUT, fn.replace(".json", ".html")), "w",
                encoding="utf-8").write(clean(d["html"]))
        n += 1
    print("清洗完成:", n, "篇")


if __name__ == "__main__":
    main()
