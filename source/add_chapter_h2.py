#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给 quantities.html 补"章级 h2 分隔"。

之前版本的 bug：把 h2 插到了 <div class="art-h"> 内部（条目标题框里），
和 "1.1 xxx" 挤在一起，没形成章节分隔效果。

正确做法：
  在每章第一个 <div class="art" ...> 之前插 <h2 class="chapter-title">
  这样形成视觉分隔：

  <h2 class="chapter-title">第 1 章 引言</h2>      ← 章节分隔条
  <div class="art">                               ← 条目 1.1
    <div class="art-h"><span>1.1</span><h3>...</h3>
  <div class="art">                               ← 条目 1.2
    ...
  <h2 class="chapter-title">第 2 章 项目数据管理</h2>
  <div class="art">                               ← 条目 2.1
    ...
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

CHAPTER_NAMES = {
    "quantities.html": {
        "1": ("引言", "Introduction"),
        "2": ("项目数据管理", "Project Data Management"),
        "3": ("工程量清单", "Bill of Quantities"),
        "4": ("定义度量", "Defining Measurements"),
        "5": ("生成工程量", "Generating Quantities"),
        "6": ("审计", "Auditing"),
        "7": ("算量表达式参考", "Quantities Expressions Reference"),
        "8": ("计算函数", "Calculation Functions"),
        "9": ("计算运算符", "Calculation Operators"),
    },
}


def _protect(text, prefix, pattern):
    mp = {}
    def _save(m):
        k = f'\x00{prefix}{len(mp)}\x00'
        mp[k] = m.group(0)
        return k
    return re.sub(pattern, _save, text, flags=re.S), mp


def add_chapter_h2(path, chapters):
    text = io.open(path, encoding="utf-8").read()
    original = text

    # 保护非正文 + 已有 <a>，防止误伤
    text, mp = _protect(text, 'H', r'<head\b[^>]*>.*?</head>')
    text = _restore(text, mp)
    text, mp_s = _protect(text, 'S', r'<style\b[^>]*>.*?</style>')
    text, mp_j = _protect(text, 'J', r'<script\b[^>]*>.*?</script>')
    text, mp_l = _protect(text, 'L', r'<link\b[^>]*/?>')
    text, mp_c = _protect(text, 'C', r'<(code|pre)\b[^>]*>.*?</\1>')
    text, mp_a = _protect(text, 'A', r'<a\b[^>]*>.*?</a>')

    # ===== 1. 收集每章第一个 .art 的 start offset =====
    # 匹配：<div class="art" ...> 紧跟的第一个 h3 编号
    first_arts = {}
    for m in re.finditer(
        r'<div\s+class="art"[^>]*>[\s\S]{0,300}?<h3[^>]*>\s*(\d+)\.(\d+)',
        text
    ):
        ch_num = m.group(1)
        if ch_num not in first_arts:
            first_arts[ch_num] = m.start()  # 这个 div 的起始位置

    print(f"找到 {len(first_arts)} 个章起始 art 块")

    # ===== 2. 倒序插入 h2（倒序避免 offset 变化） =====
    changes = 0
    for ch_num in sorted(first_arts.keys(), key=int, reverse=True):
        zh_name, en_name = chapters[ch_num]
        pos = first_arts[ch_num]

        insert = (
            f'<h2 id="s-{ch_num}" class="chapter-title zh-only block">'
            f'第 {ch_num} 章 {zh_name}</h2>\n'
            f'<h2 id="s-{ch_num}-en" class="chapter-title en-only block">'
            f'Chapter {ch_num} {en_name}</h2>\n'
        )
        text = text[:pos] + insert + text[pos:]
        changes += 1
        print(f"  Ch{ch_num}: 在 offset {pos} 前插入")

    # ===== 3. 还原保护 =====
    for mp in [mp, mp_s, mp_j, mp_l, mp_c, mp_a]:
        for k, v in mp.items():
            text = text.replace(k, v)

    # ===== 4. 注入 .chapter-title CSS =====
    # 找 <style> 里的 h3{ 规则，在它后面插 .chapter-title
    style_inject = (
        "\n/* ===== 章节级 h2 分隔 ===== */\n"
        "h2.chapter-title{font-size:clamp(18px,2.2vw,22px);font-weight:700;"
        "margin:48px 0 16px;padding:14px 20px;border-left:4px solid var(--accent);"
        "background:linear-gradient(90deg,rgba(47,111,143,.06),transparent);"
        "letter-spacing:.02em;color:var(--ink)}\n"
        "h2.chapter-title[id^='s-']{margin-top:32px}\n"
    )
    if ".chapter-title" not in text:
        text = re.sub(r'(h3\{font-size:17px;\})',
                      r'\1' + style_inject.replace('\\', '\\\\'),
                      text, count=1)
        print("  ✓ 注入 .chapter-title CSS")

    if text != original:
        io.open(path, "w", encoding="utf-8").write(text)
        print(f"\n✓ {os.path.basename(path)}: {changes} 个章 h2 已插入")
        return True
    print("\n- 无变化")
    return False


def _restore(text, mp):
    for k, v in mp.items():
        text = text.replace(k, v)
    return text


def main():
    targets = sys.argv[1:] or ["quantities.html"]
    changed = 0
    for f in targets:
        path = os.path.join(SITE, f)
        chapters = CHAPTER_NAMES.get(f)
        if not chapters:
            print(f"跳过 {f}：无章名表")
            continue
        if add_chapter_h2(path, chapters):
            changed += 1
    print(f"\n完成：{changed}/{len(targets)} 文件")


if __name__ == "__main__":
    main()
