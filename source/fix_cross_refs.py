#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给 h3 标题加锚点 id，并把 "见第 x.x.x 节" / "See section x.x.x" 等交叉引用换成可点击链接。

规则：
1. <h3 class="zh-only block">3.2.1 如何添加...</h3>  ->  <h3 id="s-3-2-1" class="zh-only block">3.2.1 如何添加...</h3>
   同一段的 <h3 class="en-only block">3.2.1 How to add...</h3>  ->  <h3 id="s-3-2-1-en" class="en-only block">3.2.1 How to add...</h3>
2. "见第 3.2.1 节" / "参见第 3.2.1 节" / "详见第 3.2.1 节" / "更多细节见第 3.2.1 节"
   -> 把数字部分抽出来转成 <a href="#s-3-2-1">见第 3.2.1 节</a>
3. "See section 3.2.1" / "refer to section 3.2.7" / "sections 3.2.3 and 3.2.7"
   -> 把每个数字都分别包成 <a href="#s-3-2-1">section 3.2.1</a>
4. 支持一条句子里有多个 section，比如 "sections 3.2.3 and 3.2.7"
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

# ----- 1. 给 h3 加 id -----
def add_h3_ids(text):
    count = 0

    # 中文 h3: 先匹配已经有 id 的（跳过），没 id 的才加
    zh_h3 = re.compile(
        r'(<h3)(?!\s+id=)(\s+class="zh-only block">)(\d+(?:\.\d+)*)\s'
    )
    def zh_replace(m):
        nonlocal count
        count += 1
        return f'{m.group(1)} id="s-{m.group(3).replace(".", "-")}"{m.group(2)}{m.group(3)} '
    text = zh_h3.sub(zh_replace, text)

    # 英文 h3: 紧跟同一个 div 里的 h3，加 id="s-x-x-x-en"
    en_h3 = re.compile(
        r'(<h3)(?!\s+id=)(\s+class="en-only block">)(\d+(?:\.\d+)*)\s'
    )
    def en_replace(m):
        nonlocal count
        count += 1
        return f'{m.group(1)} id="s-{m.group(3).replace(".", "-")}-en"{m.group(2)}{m.group(3)} '
    text = en_h3.sub(en_replace, text)

    return text, count


# ----- 2. 把数字章节引用换成锚点链接 -----
def num_to_id(num):
    """3.2.1 -> s-3-2-1"""
    return "#s-" + num.replace(".", "-")

# 中文：见第 3.2.1 节 / 参见第 3.2.1 节 / 详见第 3.2.1 节 / 更多细节见第 3.2.1 节
#      sections 3.2.3 and 3.2.7 这种带"和"/"与"的
# 中文：只替换带小数点的（比如 3.2.1 / 5.2.5），裸数字 5 不处理
ZH_SECTION_RE = re.compile(r'(第\s*)(\d+(?:\.\d+)+)(\s*节)')

# 英文：see section 3.2.1 / section 3.2.1 for more detail / sections 3.2.3 and 3.2.7
EN_PATTERNS = [
    # "section 3.2.1" 或者 "sections 3.2.3 and 3.2.7"
    (re.compile(r'section\s+(\d+(?:\.\d+)*)', re.IGNORECASE), None),
]

def zh_link_decimal(text):
    """中文带小数点：第 3.2.1 节 -> <a href="#s-3-2-1">"""
    def repl(m):
        num = m.group(2)
        return f'{m.group(1)}<a href="{num_to_id(num)}" class="xref" onclick="history.scrollRestoration=\'auto\'">{num}</a>{m.group(3)}'
    return ZH_SECTION_RE.sub(repl, text)


def _protect_xrefs(text):
    """把所有 <a class="xref" ...>...</a> 替换成占位符，避免被后续正则二次匹配"""
    protect_map = {}
    def _save(m):
        key = f'\x00XREF{len(protect_map)}\x00'
        protect_map[key] = m.group(0)
        return key
    # 贪婪匹配最近的 </a>（section 1.3 断行时仍能完整包住）
    protected = re.sub(r'<a\b[^>]*class="[^"]*xref[^"]*"[^>]*>.*?</a>', _save, text, flags=re.S)
    return protected, protect_map


def _restore(text, protect_map):
    for k, v in protect_map.items():
        text = text.replace(k, v)
    return text


def zh_link_plain(text, h3_ids):
    """中文裸数字：第 5 节 -> 跳到 #s-5-1（该章首个子节）。
    前提：调用前所有 <a class="xref"> 已被保护为占位符。"""
    plain_re = re.compile(r'(第\s*)(\d+)(\s*节)')
    def repl(m):
        num = m.group(2)
        target = f"#s-{num}-1"
        if target.lstrip("#") not in h3_ids:
            return m.group(0)  # 该章没有子节，不替换
        return f'{m.group(1)}<a href="{target}" class="xref" onclick="history.scrollRestoration=\'auto\'">{num}</a>{m.group(3)}'
    return plain_re.sub(repl, text)


def en_link_plain(text, h3_ids):
    """英文裸数字：section 5 / sections 3 and 4 -> #s-5-1 / #s-3-1, #s-4-1。
    前提：调用前所有 <a class="xref"> 已被保护为占位符。"""
    # 复数：sections N and M
    def repl_multi(m):
        a, sep, b = m.group(1), m.group(2), m.group(3)
        ta = f"#s-{a}-1" if f"s-{a}-1" in h3_ids else None
        tb = f"#s-{b}-1" if f"s-{b}-1" in h3_ids else None
        if not ta or not tb:
            return m.group(0)
        return f'<a href="{ta}" class="xref">section {a}</a> {sep} <a href="{tb}" class="xref">section {b}</a>'
    text = re.sub(
        r'sections\s+(\d+)\s+(and|or|,)\s+(\d+)',
        repl_multi, text, flags=re.IGNORECASE
    )

    # 单数：section N（后面可能跟 Em 标题，如 "section 5, <em>xxx</em>"）
    def repl_single(m):
        num = m.group(1)
        target = f"#s-{num}-1"
        if target.lstrip("#") not in h3_ids:
            return m.group(0)
        return f'<a href="{target}" class="xref">{m.group(0)}</a>'
    text = re.sub(r'\bsection\s+(\d+)\b', repl_single, text, flags=re.IGNORECASE)
    return text

def en_link(text):
    """把英文 section 数字包成链接，避免嵌套。

    两步：先处理复数 "sections X and Y"（整体替换成两个独立链接），
    再用占位符保护已有的 <a>...</a>，最后处理单数。
    """
    # 1) 复数 -> 两个独立链接
    def repl_multi(m):
        a, sep, b = m.group(1), m.group(2), m.group(3)
        return f'<a href="{num_to_id(a)}" class="xref">section {a}</a> {sep} <a href="{num_to_id(b)}" class="xref">section {b}</a>'
    text = re.sub(
        r'sections\s+(\d+(?:\.\d+)+)\s+(and|or|,)\s+(\d+(?:\.\d+)+)',
        repl_multi, text, flags=re.IGNORECASE
    )

    # 2) 保护已有的 <a ...>...</a>，替换成占位符
    placeholders = []
    def protect(m):
        placeholders.append(m.group(0))
        return f'\x00REF{len(placeholders)-1}\x00'
    text = re.sub(r'<a\b[^>]*>.*?</a>', protect, text)

    # 3) 对剩余纯文本里的单数 section 做替换
    def repl_single(m):
        num = m.group(1)
        return f'<a href="{num_to_id(num)}" class="xref">{m.group(0)}</a>'
    text = re.sub(r'section\s+(\d+(?:\.\d+)+)', repl_single, text, flags=re.IGNORECASE)

    # 4) 还原占位符
    for i, a in enumerate(placeholders):
        text = text.replace(f'\x00REF{i}\x00', a)

    return text


def process_file(path):
    text = io.open(path, encoding="utf-8").read()
    original = text

    # Step 1: 给 h3 加 id
    text, h3_count = add_h3_ids(text)

    # 收集本页所有 h3 锚点（裸数字处理时用来判断 #s-N-1 是否存在）
    h3_ids = set(re.findall(r'<h3\b[^>]*\sid="(s-[\d\-]+)"', text))

    # Step 2: 替换带小数点的交叉引用（小数章节号，精确对应 h3）
    text = zh_link_decimal(text)
    text = en_link(text)

    # Step 2.5: 保护所有已生成的 <a class="xref">，避免裸数字正则在标签内部二次匹配
    text, protect_map = _protect_xrefs(text)

    # Step 3: 替换裸数字章节引用（跳到该章首个子节）
    text = zh_link_plain(text, h3_ids)
    text = en_link_plain(text, h3_ids)

    # Step 3.5: 还原被保护的 xref
    text = _restore(text, protect_map)

    if text != original:
        io.open(path, "w", encoding="utf-8").write(text)
        print(f"  {os.path.basename(path)}: +{h3_count} h3 ids, cross refs replaced")
        return True
    else:
        print(f"  {os.path.basename(path)}: no changes needed")
        return False


def main():
    files = sys.argv[1:] if len(sys.argv) > 1 else sorted([
        os.path.join(SITE, f) for f in os.listdir(SITE) if f.endswith(".html")
    ])
    changed = 0
    for path in files:
        if process_file(path):
            changed += 1
    print(f"\nDone: {changed}/{len(files)} files modified")


if __name__ == "__main__":
    main()
