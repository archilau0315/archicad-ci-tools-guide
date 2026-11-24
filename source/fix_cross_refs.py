#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给 h3 加锚点 id，把裸文本章节引用换成可点击 <a class="xref">。

三层防误伤策略：
1. 非正文区域（<head>、<style>、<script>、<link>、<code>、<pre>）先 protect
2. 所有替换 regex 都带明确的章节引用关键字（section/see/第/节/章/详见...）
3. 分三阶段替换，每阶段结束 protect 新生成的 <a>
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))


# ---------- 1. h3 加 id ----------
def add_h3_ids(text):
    count = 0
    zh_re = re.compile(r'(<h3)(?!\s+id=)(\s+class="zh-only block">)(\d+(?:\.\d+)*)\s')
    def zh(m):
        nonlocal count; count += 1
        return f'{m.group(1)} id="s-{m.group(3).replace(".", "-")}"{m.group(2)}{m.group(3)} '
    text = zh_re.sub(zh, text)

    en_re = re.compile(r'(<h3)(?!\s+id=)(\s+class="en-only block">)(\d+(?:\.\d+)*)\s')
    def en(m):
        nonlocal count; count += 1
        return f'{m.group(1)} id="s-{m.group(3).replace(".", "-")}-en"{m.group(2)}{m.group(3)} '
    text = en_re.sub(en, text)
    return text, count


# ---------- 2. protect / restore ----------
def _protect_block(text, pattern, prefix='B'):
    """保护一个区域。prefix 区分不同阶段，避免 key 冲突。"""
    mp = {}
    def _save(m):
        k = f'\x00{prefix}{len(mp)}\x00'
        mp[k] = m.group(0)
        return k
    protected = re.sub(pattern, _save, text, flags=re.S | re.I)
    return protected, mp

def _restore_all(text, *maps):
    for mp in maps:
        for k, v in mp.items():
            text = text.replace(k, v)
    return text


# ---------- 3. 辅助 ----------
def _to_id(num):
    return "#s-" + num.replace(".", "-")

def _bid(num):
    return f"s-{num}-1"


# ---------- 4. 核心替换 ----------
def apply_all(text, h3_ids):
    """text 里非正文区域和原始 <a> 都已是占位符。"""
    protect_chain = []
    _stage = [0]  # 用列表包装以便内部修改

    def _protect_new():
        nonlocal text
        _stage[0] += 1
        prefix = f'P{_stage[0]}'
        mp = {}
        def _save(m):
            k = f'\x00{prefix}{len(mp)}\x00'
            mp[k] = m.group(0)
            return k
        text = re.sub(r'<a\b[^>]*>.*?</a>', _save, text, flags=re.S)
        protect_chain.append(mp)

    # ================================================================
    # 阶段 1A：复数/范围（匹配多编号，必须先跑，否则单数正则会抢先匹配）
    # ================================================================

    # 1Aa. 范围引用 — 英文 to（允许中间夹 <em>...</em> 等标签）
    def r_en(m):
        a, b = m.group(1), m.group(2)
        a_t = _to_id(a) if "." in a else f"#s-{a}-1"
        b_t = _to_id(b) if "." in b else f"#s-{b}-1"
        return (f'<a href="{a_t}" class="xref">{a}</a> to '
                f'<a href="{b_t}" class="xref">{b}</a>')
    text = re.sub(
        r'(\d+(?:\.\d+)*)\s+(?:<[^>]*>[^<]*</[^>]*>\s*)*to\s+'
        r'(\d+(?:\.\d+)+)',
        r_en, text, flags=re.I
    )
    # 1Ab. 范围引用 — 中文 至/到/~
    def r_zh(m):
        a, sep, b = m.group(1), m.group(2), m.group(3)
        a_t = _to_id(a) if "." in a else f"#s-{a}-1"
        b_t = _to_id(b) if "." in b else f"#s-{b}-1"
        return (f'<a href="{a_t}" class="xref">{a}</a> {sep} '
                f'<a href="{b_t}" class="xref">{b}</a>')
    text = re.sub(
        r'(\d+(?:\.\d+)*)\s*(至|到|~)\s*(\d+(?:\.\d+)+)',
        r_zh, text
    )

    # 1Ac. 英文复数 — 允许中间夹 (...) 或 <em>...</em> 或逗号
    def en_pl(m):
        p, a, sep, b = m.group(1), m.group(2), m.group(3), m.group(4)
        a_t = _to_id(a) if "." in a else f"#s-{a}-1"
        b_t = _to_id(b) if "." in b else f"#s-{b}-1"
        if "." not in a and _bid(a) not in h3_ids: return m.group(0)
        if "." not in b and _bid(b) not in h3_ids: return m.group(0)
        return (f'<a href="{a_t}" class="xref">{p} {a}</a> {sep} '
                f'<a href="{b_t}" class="xref">{b}</a>')
    text = re.sub(
        r'(sections?)\s+(\d+(?:\.\d+)*)'
        r'(?:\s*\([^)]*\)|\s*<[^>]*>[^<]*</[^>]*>|\s*,\s*[^,]*?)?'
        r'\s+(and|or|,|、)\s+'
        r'(\d+(?:\.\d+)*)',
        en_pl, text, flags=re.I
    )

    # ---- 阶段 1A protect：所有多编号引用的产物 ----
    _protect_new()

    # ================================================================
    # 阶段 1B：单数精确匹配（此时 1A 的产物已是占位符，不会被二次匹配）
    # ================================================================

    # 1c. 中文 "第 X 章/节" — 裸数字
    def zh_p1(m):
        num = m.group(1)
        t = f"#s-{num}-1"
        if _bid(num) not in h3_ids: return m.group(0)
        return f'第 <a href="{t}" class="xref">{num}</a>' + m.group(2)
    text = re.sub(r'第\s*(\d+)\s*(章|节)', zh_p1, text)

    # 1c2. 中文 "第 X.X.X 节" — 带小数点
    def zh_d1(m):
        num = m.group(1)
        return f'第 <a href="{_to_id(num)}" class="xref">{num}</a>' + m.group(2)
    text = re.sub(r'第\s*(\d+(?:\.\d+)+)\s*(章|节)', zh_d1, text)

    # 1c3. 中文 "X.X.X 节" — 无前缀
    def zh_d2(m):
        num = m.group(1)
        return f'<a href="{_to_id(num)}" class="xref">{num}</a>' + m.group(2)
    text = re.sub(r'(\d+(?:\.\d+)+)\s*(章|节)', zh_d2, text)

    # 1d. 英文 section(s) + 小数
    def sec_dec(m):
        return f'<a href="{_to_id(m.group(2))}" class="xref">{m.group(0)}</a>'
    text = re.sub(
        r'\b(sections?)\s+(\d+(?:\.\d+)+)',
        sec_dec, text, flags=re.I
    )

    # 1e. 英文 see/refer to + 小数
    def see_dec(m):
        kw, num = m.group(1), m.group(2)
        return f'{kw} <a href="{_to_id(num)}" class="xref">{num}</a>'
    text = re.sub(
        r'\b(see|refer to)\s+(\d+(?:\.\d+)+)',
        see_dec, text, flags=re.I
    )

    # ---- 阶段 1 protect ----
    _protect_new()

    # ================================================================
    # 阶段 2：宽泛匹配（裸数字 section、引导词+裸编号）
    # ================================================================

    # 2a. 英文 see/refer to + 裸数字
    def see_plain(m):
        kw, num = m.group(1), m.group(2)
        t = f"#s-{num}-1"
        if _bid(num) not in h3_ids: return m.group(0)
        return f'{kw} <a href="{t}" class="xref">{num}</a>'
    text = re.sub(
        r'\b(see|refer to)\s+(\d+)\b',
        see_plain, text, flags=re.I
    )

    # 2b. 英文 section(s) + 裸数字
    def sec_plain(m):
        num = m.group(2)
        t = f"#s-{num}-1"
        if _bid(num) not in h3_ids: return m.group(0)
        return f'<a href="{t}" class="xref">{m.group(0)}</a>'
    text = re.sub(
        r'\b(sections?)\s+(\d+)\b',
        sec_plain, text, flags=re.I
    )

    # 2c. 中文引导词 + 小数（表头 "详见 2.3.1"、"见 2.3.8" 等，无"节"字）
    def zh_tail(m):
        lead, num = m.group(1), m.group(2)
        return f'{lead}<a href="{_to_id(num)}" class="xref">{num}</a>'
    text = re.sub(
        r'(详见|参见|另请参见|更多细节见|见)\s*(\d+(?:\.\d+)+)',
        zh_tail, text
    )

    # ---- 阶段 2 protect ----
    _protect_new()

    # ================================================================
    # 阶段 3：安全兜底（and/逗号 后裸小数，h3_ids 校验防误伤）
    #   此时 CSS/JS/原始 <a> 都是占位符，纯文本里只有正文内容
    # ================================================================
    def safe_dec(m):
        lead, num = m.group(1), m.group(2)
        dec_id = _to_id(num).lstrip('#') if '.' in num else _bid(num)
        if dec_id not in h3_ids:
            return m.group(0)
        return f'{lead}<a href="{_to_id(num)}" class="xref">{num}</a>'
    # and/to/逗号 后 + 小数编号 + 逗号/句号/括号/结尾
    text = re.sub(
        r'((?:\band\b|\bto\b|,)\s+)(\d+(?:\.\d+){1,3})(?=[,.)]|$)',
        safe_dec, text, flags=re.I
    )

    def safe_plain(m):
        lead, num = m.group(1), m.group(2)
        t = f"#s-{num}-1"
        if _bid(num) not in h3_ids: return m.group(0)
        return f'{lead}<a href="{t}" class="xref">{num}</a>'
    # and/逗号 后 + 裸数字 1-9 + 逗号/句号/括号
    text = re.sub(
        r'((?:\band\b|,)\s+)([1-9])(?=[,.)])',
        safe_plain, text, flags=re.I
    )

    # 还原所有保护
    for mp in reversed(protect_chain):
        for k, v in mp.items():
            text = text.replace(k, v)

    return text


# ---------- 5. 入口 ----------
def process_file(path):
    text = io.open(path, encoding="utf-8").read()
    original = text

    text, h3_count = add_h3_ids(text)
    h3_ids = set(re.findall(r'<h3\b[^>]*\sid="(s-[\d\-]+)"', text))

    # ---- 先保护非正文区域（每个用不同 prefix 防 key 冲突）----
    protected_blocks = []
    text, mp = _protect_block(text, r'<head\b[^>]*>.*?</head>', 'H')
    protected_blocks.append(mp)
    text, mp = _protect_block(text, r'<style\b[^>]*>.*?</style>', 'S')
    protected_blocks.append(mp)
    text, mp = _protect_block(text, r'<script\b[^>]*>.*?</script>', 'J')
    protected_blocks.append(mp)
    text, mp = _protect_block(text, r'<link\b[^>]*/?>', 'L')
    protected_blocks.append(mp)
    text, mp = _protect_block(text, r'<(code|pre)\b[^>]*>.*?</\1>', 'C')
    protected_blocks.append(mp)

    # ---- 再保护原始 <a> ----
    text, anchor_map = _protect_block(text, r'<a\b[^>]*>.*?</a>', 'A')
    protected_blocks.append(anchor_map)

    # ---- 替换章节引用 ----
    text = apply_all(text, h3_ids)

    # ---- 还原所有保护（反向）----
    text = _restore_all(text, *reversed(protected_blocks))

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
