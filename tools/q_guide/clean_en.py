# -*- coding: utf-8 -*-
"""清洗官方 Word 导出 HTML：去掉 font/span 包装与内联样式，保留语义标签。

输入：tools/q_guide/raw/{id}.json（html 字段）
输出：tools/q_guide/en_clean/{id}.html
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "en_clean")

KEEP = {"p", "em", "strong", "b", "i", "ul", "ol", "li", "h1", "h2", "h3", "h4",
        "img", "a", "table", "thead", "tbody", "tr", "td", "th", "br", "blockquote"}


def clean(html):
    # 去 script/style
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S | re.I)
    # <font> <span> 直接拆包装（保留内部内容）
    while re.search(r"<(font|span)\b[^>]*>", html):
        html = re.sub(r"<(font|span)\b[^>]*>(.*?)</\1>", r"\2", html, flags=re.S | re.I)
    # 去所有标签属性（img/a 保留必要属性）
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
    # 空 p 清理
    html = re.sub(r"<p>\s*</p>", "", html)
    # 连续空行压一行
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def main():
    os.makedirs(OUT, exist_ok=True)
    for fn in sorted(os.listdir(RAW)):
        if not fn.endswith(".json"):
            continue
        d = json.load(io.open(os.path.join(RAW, fn), encoding="utf-8"))
        io.open(os.path.join(OUT, fn.replace(".json", ".html")), "w",
                encoding="utf-8").write(clean(d["html"]))
    print("清洗完成:", len(os.listdir(OUT)), "篇")


if __name__ == "__main__":
    main()
