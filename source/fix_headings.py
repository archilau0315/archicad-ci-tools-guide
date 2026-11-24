#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复正文顶级 h2/h3 裸中文标题。

扫描规则：在每个 HTML 的 <main> 区域里，找直接包含中文的 h2/h3，
且该标签自身不含 zh-only/en-only 包裹。
不碰 sidebar/nav-h/已包裹的。
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

HAS_ZH = re.compile(r'[\u4e00-\u9fff]')

# ===== 每个页面的 h2/h3 中英文对照 =====
# 格式：中文 → 英文（用于替换时生成 en-only 版本）
ZH_TO_EN = {
    # index.html
    "开始使用": "Get Started",
    # 常见通用
    "总览": "Overview",
    "引言": "Introduction",
    "目录": "Contents",
    "参考": "References",
    "附录": "Appendix",
    "术语": "Terminology",
    "常见问题": "FAQ",
    "作者": "Credits",
    "许可": "License",
    "更新日志": "Changelog",
    "正文": "Main content",
}


def wrap_heading(open_tag, text, en_text):
    """把裸中文标题包装成 zh-only + en-only 双语版本"""
    # open_tag 形如 <h2> 或 <h3 id="xxx" class="xxx">
    tag_match = re.match(r'<(h[23])(\s[^>]*)?>', open_tag)
    if not tag_match:
        return None
    tag = tag_match.group(1)
    attrs = tag_match.group(2) or ""
    attrs_no_lang = re.sub(r'\sclass="[^"]*zh-only[^"]*"', '', attrs)
    attrs_no_lang = re.sub(r'\sclass="[^"]*en-only[^"]*"', '', attrs_no_lang)
    attrs_no_lang = attrs_no_lang.strip()
    # 保留 class 属性（如果有其他 class）
    if attrs_no_lang:
        new_open = f'<{tag}{attrs_no_lang}>'
    else:
        new_open = f'<{tag}>'
    return f'{new_open}<span class="zh-only">{text}</span><span class="en-only">{en_text}</span>'


def fix_file(path):
    t = io.open(path, encoding="utf-8").read()
    original = t
    fname = os.path.basename(path)

    # 限定在 <main> 区域内（sidebar 在 aside 里，已处理过）
    m_main = re.search(r'<main\b[^>]*>([\s\S]*?)</main>', t)
    if not m_main:
        return None
    main_start = m_main.start() + m_main.group(0).find('<main')
    inner_start = m_main.start() + m_main.group(0).find('>') + 1
    inner_end = m_main.end() - len('</main>')
    main_inner = t[inner_start:inner_end]
    offset_delta = inner_start  # 映射 main_inner 内位置 → 全文位置

    changes = 0

    # 找 main 里直接包含中文的 h2/h3（标签自身不含 zh-only）
    pattern = re.compile(
        r'<(h[23])(\s[^>]*)?>([\s\S]*?)</\1>',
        re.S
    )
    for m in pattern.finditer(main_inner):
        open_tag = m.group(0)[:m.group(0).find('>')+1]
        content = m.group(3).strip()
        # 只处理：有中文 + 标签内没 zh-only
        if not HAS_ZH.search(content):
            continue
        if 'zh-only' in m.group(0):
            continue
        # 标签内除了文本还有别的子元素（如 <span class="pkg">）时跳过
        # 只处理纯文本标题
        if re.search(r'<(span|b|strong|em)[^>]*>', content):
            # 尝试只处理其中的纯文本部分
            plain = re.sub(r'<[^>]+>', '', content).strip()
            if not HAS_ZH.search(plain):
                continue
            # 如果 span 是 pkg/徽标之类，跳过整体处理
            if re.search(r'<span class="pkg', content):
                continue
            # 其他情况：文本里混了 span 子元素，跳过（需要手动处理）
            continue

        # 纯中文标题，找英文翻译
        en = ZH_TO_EN.get(content)
        if not en:
            # 自动翻译：粗略音译/保留中文结构（仅做占位）
            # 对于 index.html 的已知标题，我们显式映射
            continue

        # 替换
        new_inner = wrap_heading(open_tag, content, en)
        if new_inner:
            abs_start = main_start + m.start()
            abs_end = main_start + m.end()
            t = t[:abs_start] + new_inner + t[abs_end:]
            changes += 1

    if t != original:
        io.open(path, "w", encoding="utf-8").write(t)
        return changes, fname
    return None


def main():
    html_files = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    for fname in html_files:
        path = os.path.join(SITE, fname)
        result = fix_file(path)
        if result:
            n, f = result
            print(f"  ✓ {f}: {n} 处")
        else:
            print(f"  - {fname}: 无变化")


if __name__ == "__main__":
    main()
