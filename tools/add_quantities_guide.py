# -*- coding: utf-8 -*-
"""把官方 Quantities 手册第 1、2 章共 22 篇注入教程站。

数据来自 tools/q_guide/articles.json（fetch_quantities_guide.py 抓取 + 人工翻译）。
插入位置：quantities.html 分册 <article> 最前（手册章节 1.x/2.x 排在现有 2.4.7 之前，
正好与已有的第 3-9 章衔接）。同步更新 quantities / index / all / about 计数与 toc。

幂等：quantities.html 已含 a-360001245296 则跳过插入，仅校正计数。
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, "site")
DATA = json.load(io.open(os.path.join(HERE, "q_guide", "articles.json"), encoding="utf-8"))
N = len(DATA)
IMG_ADD = 13        # 新增图片数
WORDS_ADD = (sum(len(a["en_body"]) + len(a["zh_body"]) for a in DATA)) / 10000.0


def block(a):
    return f"""<div class="art" id="a-{a['id']}">
  <div class="art-h"><span class="no">{a['no']}</span>
    <h3 class="zh-only block">{a['zh']}</h3>
    <h3 class="en-only block">{a['en']}</h3>
  </div>
  <div class="art-src"><a href="{a['src']}" target="_blank" rel="noopener">MyCi 官方原文 ↗</a></div>
  <div class="zh-only">{a['zh_body']}</div>
  <div class="en-only">{a['en_body']}</div>
  <details class="orig-toggle">
    <summary><span class="zh-only">英文原文对照</span><span class="en-only">Official English Original</span></summary>
    <div class="orig-body">
      <div class="orig-label"><span class="zh-only">官方英文原文</span><span class="en-only">Official English Original</span></div>
      {a['en_body']}
    </div>
  </details>
</div>
"""


def toc_item(a):
    return (f'<li><a href="quantities.html#a-{a["id"]}"><span class="tg">{a["no"]}</span>'
            f'<span class="zh-only">{a["zh"]}</span><span class="en-only">{a["en"]}</span></a></li>')


def rw(name):
    p = os.path.join(SITE, name)
    return p, io.open(p, encoding="utf-8").read()


def inject_quantities():
    p, h = rw("quantities.html")
    if 'id="a-360001245296"' not in h:
        payload = "\n".join(block(a) for a in DATA)
        h = h.replace("<article>", "<article>\n" + payload, 1)
        print(f"  quantities: 已插入 {N} 篇")
    else:
        print("  quantities: 已存在，跳过插入")
    # hero 计数 100 篇 / 9.8 万字 / 28 图
    h = re.sub(r'(<span><b>)100(</b> <span class="zh-only">篇教程)', r"\g<1>122\g<2>", h, count=1)
    h = re.sub(r'(<span><b>)9\.8(</b> <span class="zh-only">万字)',
               r"\g<1>" + f"{9.8 + WORDS_ADD:.1f}" + r"\g<2>", h, count=1)
    h = re.sub(r'(<span><b>)28(</b> <span class="zh-only">张图)', r"\g<1>41\g<2>", h, count=1)
    io.open(p, "w", encoding="utf-8").write(h)


def inject_toc():
    items = "".join(toc_item(a) for a in DATA)
    for name in ("index.html", "all.html"):
        p, h = rw(name)
        if 'quantities.html#a-360001245296' not in h:
            m = re.search(r'(<h2>Quantities.*?</h2>\s*<ul class="toc-list">)(.*?)(</ul>)', h, re.S)
            if m:
                h = h[: m.start(2)] + items + m.group(2) + h[m.end(2):]
                print(f"  {name}: toc 已前置 {N} 项")
            else:
                print(f"  {name}: 未找到 Quantities toc 块！")
        io.open(p, "w", encoding="utf-8").write(h)


INLINE_CSS = ('.art img.inl{display:inline-block;vertical-align:-0.35em;margin:0 3px;'
              'max-width:1.7em;max-height:1.7em;border-radius:3px;box-shadow:none}')


def fix_inline_imgs():
    """小按钮图（宽<60px）在正文里应随文排列，不被全局 img 样式拉成独占一行。"""
    from PIL import Image
    p, h = rw("quantities.html")
    if INLINE_CSS not in h:
        h = h.replace("img{max-width:100%", INLINE_CSS + "\nimg{max-width:100%", 1)
    for src in set(re.findall(r'<img src="(img/[^"]+)"', h)):
        path = os.path.join(SITE, src)
        if not os.path.exists(path):
            continue
        if Image.open(path).size[0] < 60:
            h = h.replace(f'<img src="{src}"', f'<img class="inl" src="{src}"')
    io.open(p, "w", encoding="utf-8").write(h)
    print("  小图标已改为随文排列")


def fix_counts():
    imgs = 1214 + IMG_ADD
    words = 42.5 + WORDS_ADD
    repl = {
        "360 篇文档、1214 张界面截图": f"382 篇文档、{imgs} 张界面截图",
        "共 360 篇，点标题直达分册的具体文章。": "共 382 篇，点标题直达分册的具体文章。",
        "共 360 篇教程（357 篇官方原文 + 3 篇 AC30 补写），按工具分册列出。":
            "共 382 篇教程（379 篇官方原文 + 3 篇 AC30 补写），按工具分册列出。",
        "All 360 articles (357 official plus 3 written for AC30), listed by tool.":
            "All 382 articles (379 official plus 3 written for AC30), listed by tool.",
        "共 357 篇官方文档、1208 张界面截图": f"共 379 篇官方文档、{imgs} 张界面截图",
    }
    for name in ("index.html", "all.html", "about.html"):
        p, h = rw(name)
        for a, b in repl.items():
            h = h.replace(a, b)
        io.open(p, "w", encoding="utf-8").write(h)

    # index hero 数字
    p, h = rw("index.html")
    h = h.replace("<b>360</b>", "<b>382</b>", 1)
    h = h.replace(f"<b>1214</b>", f"<b>{imgs}</b>", 1)
    h = h.replace("<b>42.5</b>", f"<b>{words:.1f}</b>", 1)
    # Quantities 卡片
    h = h.replace('<span class="zh-only">100 篇 · 28 图</span><span class="en-only">100 articles · 28 images</span>',
                  '<span class="zh-only">122 篇 · 41 图</span><span class="en-only">122 articles · 41 images</span>')
    io.open(p, "w", encoding="utf-8").write(h)

    # all.html pill
    p, h = rw("all.html")
    h = h.replace('<h2>Quantities · 工程量算量 <span class="pill">100 篇</span></h2>',
                  '<h2>Quantities · 工程量算量 <span class="pill">122 篇</span></h2>')
    io.open(p, "w", encoding="utf-8").write(h)

    # readme 徽章
    p = os.path.join(ROOT, "readme.md")
    h = io.open(p, encoding="utf-8").read()
    h = h.replace("articles-357-6d9470", f"articles-382-6d9470").replace(">357<", ">382<")
    h = h.replace("screenshots-1193-35613f", f"screenshots-{imgs}-35613f").replace(">1193<", f">{imgs}<")
    h = h.replace("357 篇官方文档全部译为中文、1193 张界面截图",
                  f"379 篇官方文档全部译为中文、{imgs} 张界面截图")
    io.open(p, "w", encoding="utf-8").write(h)
    print(f"  计数已更新：382 篇 / {imgs} 图 / {words:.1f} 万字（新增 {WORDS_ADD:.1f} 万）")


if __name__ == "__main__":
    print(f"新增 {N} 篇，{IMG_ADD} 图，{WORDS_ADD:.2f} 万字")
    inject_quantities()
    inject_toc()
    fix_inline_imgs()
    fix_counts()
    print("完成")
