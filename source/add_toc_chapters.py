#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在 index.html 的 Quantities 全量目录里插入章节分组。"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

CHAPTER_NAMES = {
    "1": ("引言", "Introduction"),
    "2": ("项目数据管理", "Project Data Management"),
    "3": ("工程量清单", "Bill of Quantities"),
    "4": ("定义度量", "Defining Measurements"),
    "5": ("生成工程量", "Generating Quantities"),
    "6": ("审计", "Auditing"),
    "7": ("算量表达式参考", "Quantities Expressions Reference"),
    "8": ("计算函数", "Calculation Functions"),
    "9": ("计算运算符", "Calculation Operators"),
}


def add_toc_chapter_groups(path):
    text = io.open(path, encoding="utf-8").read()
    original = text

    # 1. 定位 Quantities 区域
    m_qt = re.search(r'<h2>\s*Quantities\b', text)
    all_h2 = list(re.finditer(r'<h2>', text))
    qt_pos = m_qt.start()
    next_h2_start = None
    for m in all_h2:
        if m.start() > qt_pos:
            next_h2_start = m.start()
            break
    section_end = next_h2_start or len(text)
    section = text[qt_pos:section_end]

    # 2. 找 Quantities 的 ul 绝对边界
    m_ul_start = re.search(r'<ul class="toc-list">', section)
    ul_start = qt_pos + m_ul_start.start()
    m_ul_end = list(re.finditer(r'</ul>', section))[-1]
    ul_end = qt_pos + m_ul_end.end()

    ul_content = text[ul_start:ul_end]
    print(f"Quantities toc-list: {ul_start}-{ul_end}, 含 {ul_content.count('quantities.html')} 个链接")

    # 清理已存在的旧分隔条，保证可重复运行
    ul_content = re.sub(r'<li class="ch-divider[^"]*">[^<]*</li>', '', ul_content)

    # 3. 提取每个 <li> 的章号 + 在 ul_content 里的 offset
    li_pattern = re.compile(
        r'<li>\s*<a\s+href="quantities\.html#[^"]*"[^>]*>\s*'
        r'(?:<span class="tg">\d+</span>\s*)?'
        r'<span class="zh-only">(\d+\.\d+(?:\.\d+)?)\s*[^<]*</span>',
        re.S
    )

    li_info = []  # [(offset_in_ul, chapter_num), ...]
    for m in li_pattern.finditer(ul_content):
        ch_num = m.group(1).split('.')[0]
        li_info.append((m.start(), ch_num))

    # 有些 li 可能没匹配到（比如格式稍微不同的），补兜底
    # 简单点：直接从 href 文本里提取所有 <li> 的位置
    all_li = [(m.start(), m.group(0)) for m in re.finditer(r'<li>.*?</li>', ul_content, re.S)]
    if len(li_info) < len(all_li):
        print(f"  正则匹配 {len(li_info)}/{len(all_li)} 个 li，补兜底")
        # 兜底：从每个 li 的 zh-only span 或标题文本里提取
        offsets_with_ch = {off: ch for off, ch in li_info}
        for off, li_html in all_li:
            if off not in offsets_with_ch:
                # 尝试从 href 后面的文本提取编号
                m2 = re.search(r'(\d+)\.\d+', li_html)
                if m2:
                    offsets_with_ch[off] = m2.group(1)
        li_info = sorted(offsets_with_ch.items())

    print(f"  条目数: {len(li_info)}, 章节: {sorted(set(c for _,c in li_info), key=int)}")

    # 4. 正序遍历，记录每章【第一个】条目的 offset
    first_off = {}
    for off, ch_num in li_info:
        if ch_num not in first_off:
            first_off[ch_num] = off

    # 5. 倒序插入章节分隔 li（倒序避免 offset 位移）
    changes = 0
    for ch_num in sorted(first_off, key=int, reverse=True):
        off = first_off[ch_num]
        zh_name, en_name = CHAPTER_NAMES.get(ch_num, (f"第{ch_num}章", f"Ch{ch_num}"))
        divider = (
            f'<li class="ch-divider zh-only block">'
            f'第 {ch_num} 章 {zh_name}</li>'
            f'<li class="ch-divider en-only block">'
            f'Chapter {ch_num} {en_name}</li>'
        )
        ul_content = ul_content[:off] + divider + ul_content[off:]
        changes += 1
        print(f"  ✓ Ch{ch_num}: 在 ul offset {off} 前插入")

    # 5. 替换回 text
    text = text[:ul_start] + ul_content + text[ul_end:]

    # 6. 注入 .ch-divider CSS
    style_inject = (
        "\n/* index.html Quantities 目录章节分组 */\n"
        ".toc-list li.ch-divider{grid-column:1/-1;font-size:13px;font-weight:700;"
        "margin:18px 0 6px;padding:6px 12px;background:rgba(47,111,143,.07);"
        "border-left:3px solid var(--accent);border-radius:0 4px 4px 0;"
        "color:var(--accent);letter-spacing:.03em;list-style:none}\n"
        ".toc-list li.ch-divider.zh-only{display:inline}\n"
        ".toc-list li.ch-divider.en-only{display:none}\n"
        "html[data-lang=\"en\"] .toc-list li.ch-divider.zh-only{display:none}\n"
        "html[data-lang=\"en\"] .toc-list li.ch-divider.en-only{display:inline}\n"
    )
    if ".ch-divider" not in text:
        text = text.replace("</style>", style_inject + "</style>", 1)
        print("  ✓ 注入 .ch-divider CSS")

    if text != original:
        io.open(path, "w", encoding="utf-8").write(text)
        print(f"\n✓ 完成：{changes} 个章节分组已插入 index.html")
        return True
    print("\n- 无变化")
    return False


def main():
    path = os.path.join(SITE, "index.html")
    add_toc_chapter_groups(path)


if __name__ == "__main__":
    main()
