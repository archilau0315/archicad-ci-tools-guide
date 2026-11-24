#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给 quantities.html / metadata.html 补 h2 章标题。

策略：
- 在"每章第一个 h3"之前插一对 zh/en h2
- h2 id 规则：s-{N} 和 s-{N}-en（与现有 s-{N}-{sub} h3 体系一致）
- 同时保护非正文和已有 <a>，防误伤
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

# ====== 章名表（从 MyCi 原始 Quantities 官方文档） ======
# 格式：章节号 -> (中文名, 英文名)
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
    "metadata.html": {
        "3": ("元数据查看", "Element Metadata"),
    },
}


def _protect(text, prefix, pattern=r'<a\b[^>]*>.*?</a>'):
    mp = {}
    def _save(m):
        k = f'\x00{prefix}{len(mp)}\x00'
        mp[k] = m.group(0)
        return k
    return re.sub(pattern, _save, text, flags=re.S), mp

def _restore(text, *maps):
    for mp in maps:
        for k, v in mp.items():
            text = text.replace(k, v)
    return text


def add_chapter_h2(path, chapters):
    text = io.open(path, encoding="utf-8").read()
    original = text

    # 保护非正文 + 已有 <a>
    text, mp_h = _protect(text, 'H', r'<head\b[^>]*>.*?</head>')
    text, mp_s = _protect(text, 'S', r'<style\b[^>]*>.*?</style>')
    text, mp_j = _protect(text, 'J', r'<script\b[^>]*>.*?</script>')
    text, mp_l = _protect(text, 'L', r'<link\b[^>]*/?>')
    text, mp_c = _protect(text, 'C', r'<(code|pre)\b[^>]*>.*?</\1>')
    text, mp_a = _protect(text, 'A', r'<a\b[^>]*>.*?</a>')

    changed = 0

    # 对每章（按编号升序）：找到该章第一个 zh-only h3，在它之前插 h2
    # 注意：zh-only h3 和 en-only h3 相邻出现，插在 zh 之前即可
    for ch_num in sorted(chapters.keys(), key=int):
        zh_name, en_name = chapters[ch_num]

        # 该章第一个 h3 zh-only
        zh_pat = (
            rf'(<h3\s+id="s-{ch_num}-\d+"\s+class="zh-only block">)'
        )
        m = re.search(zh_pat, text)
        if not m:
            print(f"  ⚠ 找不到第 {ch_num} 章的 h3，跳过")
            continue

        insert = (
            f'<h2 id="s-{ch_num}" class="zh-only block">第 {ch_num} 章 {zh_name}</h2>\n'
            f'  <h2 id="s-{ch_num}-en" class="en-only block">Chapter {ch_num} {en_name}</h2>\n  '
        )
        text = text[:m.start()] + insert + text[m.start():]
        changed += 1
        print(f"  + 第 {ch_num} 章: {zh_name} / {en_name}")

    # 还原
    text = _restore(text, mp_h, mp_s, mp_j, mp_l, mp_c, mp_a)

    if text != original:
        io.open(path, "w", encoding="utf-8").write(text)
        print(f"\n✓ {os.path.basename(path)}: 插入 {changed} 个 h2 章标题")
        return True
    else:
        print(f"\n- {os.path.basename(path)}: 无变化")
        return False


def main():
    targets = sys.argv[1:] or ["quantities.html"]
    changed = 0
    for f in targets:
        path = os.path.join(SITE, f)
        if not os.path.isfile(path):
            print(f"跳过：{path} 不存在")
            continue
        chapters = CHAPTER_NAMES.get(f)
        if not chapters:
            print(f"跳过：{f} 没有章名表")
            continue
        print(f"\n处理 {f} ...")
        if add_chapter_h2(path, chapters):
            changed += 1
    print(f"\n完成：{changed}/{len(targets)} 文件修改")


if __name__ == "__main__":
    main()
