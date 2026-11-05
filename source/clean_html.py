# -*- coding: utf-8 -*-
"""把 MyCi 文章的 LibreOffice 风格 HTML 转成干净 Markdown"""
import io, re, html

def clean(body: str) -> str:
    s = body
    # 图片 → 占位标记；若图片被 <a> 包裹（图片即链接），保留链接地址
    imgs = []
    def img_sub(m):
        imgs.append(m.group(1))
        return f"\n\n%%IMG{len(imgs)-1}%%\n\n"
    # 先处理 <a ...><img ...></a>
    def a_img(m):
        url = m.group(1)
        inner = m.group(3) or ""
        im = re.search(r'src="([^"]+)"', inner)
        if im:
            # 图片本体单独编号，LINKIMG 只记外链
            imgs.append(im.group(1))
            return f"%%IMGLINK{len(imgs)-1}|{url}%%"
        return f"%%LINKIMG{url}%%"
    s = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(?:(?!</a>).)*?<img[^>]*src="([^"]+)"[^>]*(?:(?!</a>).)*?</a>',
               lambda m: f"%%IMGLINK{m.group(2)}|{m.group(1)}%%", s, flags=re.S)
    s = re.sub(r'<img[^>]*src="([^"]+)"[^>]*>', img_sub, s)
    # 链接
    def a_sub(m):
        txt = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        url = m.group(1)
        if not txt:
            txt = re.sub(r'^https?://(www\.)?', '', url).split('/')[0]
        return f"[{txt}]({url})"
    s = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', a_sub, s, flags=re.S)
    # 列表：li 内容里的段落标签先转成空格，避免拆行
    s = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: '\n- ' + re.sub(r'<[^>]+>', ' ', m.group(1)).strip() + '\n', s, flags=re.S)
    s = re.sub(r'<ul[^>]*>', '\n', s)
    s = re.sub(r'</ul>', '\n', s)
    s = re.sub(r'<ol[^>]*>', '\n', s)
    s = re.sub(r'</ol>', '\n', s)
    # 标题
    for n in range(1, 7):
        s = re.sub(rf'<h{n}[^>]*>(.*?)</h{n}>', lambda m, n=n: "\n\n" + "#"*n + " " + re.sub(r'<[^>]+>', '', m.group(1)).strip() + "\n\n", s, flags=re.S)
    # 强调
    s = re.sub(r'<strong[^>]*>(.*?)</strong>', lambda m: "**" + re.sub(r'<[^>]+>', '', m.group(1)).strip() + "**", s, flags=re.S)
    s = re.sub(r'<b[^>]*>(.*?)</b>', lambda m: "**" + re.sub(r'<[^>]+>', '', m.group(1)).strip() + "**", s, flags=re.S)
    s = re.sub(r'<em[^>]*>(.*?)</em>', lambda m: "*" + re.sub(r'<[^>]+>', '', m.group(1)).strip() + "*", s, flags=re.S)
    s = re.sub(r'<i[^>]*>(.*?)</i>', lambda m: "*" + re.sub(r'<[^>]+>', '', m.group(1)).strip() + "*", s, flags=re.S)
    # 代码
    s = re.sub(r'<code[^>]*>(.*?)</code>', lambda m: "`" + re.sub(r'<[^>]+>', '', m.group(1)).strip() + "`", s, flags=re.S)
    s = re.sub(r'<pre[^>]*>(.*?)</pre>', lambda m: "\n```\n" + re.sub(r'<[^>]+>', '', m.group(1)).strip() + "\n```\n", s, flags=re.S)
    # 表格
    def tbl(m):
        inner = m.group(1)
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', inner, flags=re.S)
        out = []
        for r in rows:
            cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, flags=re.S)
            cells = [re.sub(r'<[^>]+>', '', c).strip().replace("|", "\\|").replace("\n", " ") for c in cells]
            out.append("| " + " | ".join(cells) + " |")
        if not out: return ""
        hdr = out[0]
        sep = "| " + " | ".join(["---"] * (hdr.count("|") - 1)) + " |"
        return "\n\n" + "\n".join([hdr, sep] + out[1:]) + "\n\n"
    s = re.sub(r'<table[^>]*>(.*?)</table>', tbl, s, flags=re.S)
    # 段落与换行
    s = re.sub(r'<p[^>]*>', '\n\n', s)
    s = re.sub(r'</p>', '', s)
    s = re.sub(r'<br[^>]*/?>', '\n', s)
    s = re.sub(r'<div[^>]*>', '\n', s)
    s = re.sub(r'</div>', '\n', s)
    # 去掉所有残留标签
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    # 清理空行与缩进
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    s = "\n".join(l.rstrip() for l in s.split("\n"))
    return s.strip()

if __name__ == "__main__":
    import json, sys
    d = json.load(io.open(sys.argv[1], encoding="utf-8"))
    out = {}
    for aid, a in d.items():
        txt = clean(a["body"])
        out[aid] = {"title": a["title"], "cat": a["cat"], "md": txt,
                    "url": a["url"], "len": len(txt)}
    json.dump(out, io.open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    tot = sum(v["len"] for v in out.values())
    empty = sum(1 for v in out.values() if v["len"] < 50)
    print(f"转换 {len(out)} 篇，总 {tot/10000:.1f} 万字符，空/极短 {empty} 篇")
