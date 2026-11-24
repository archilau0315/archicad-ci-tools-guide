import re, os

for fname in ["quantities.html", "metadata.html"]:
    p = os.path.join(r"e:\works\Aidev\Kbitai绝对安全\kbitai_com_cn\resources\AC_Tutorial\ci_tools\site", fname)
    t = open(p, encoding="utf-8").read()

    # 所有 zh-only h3 的完整标题
    all_zh = re.findall(r'<h3 id="s-(\d+)-[^"]+" class="zh-only block">(.*?)</h3>', t)
    all_en = re.findall(r'<h3 id="s-(\d+)-[^"]+-en" class="en-only block">(.*?)</h3>', t)

    zh_by_ch = {}
    for ch, title in all_zh:
        if ch not in zh_by_ch:
            zh_by_ch[ch] = title.strip()

    en_by_ch = {}
    for ch, title in all_en:
        if ch not in en_by_ch:
            en_by_ch[ch] = title.strip()

    print(f"\n=== {fname} ===")
    for ch in sorted(zh_by_ch.keys(), key=int):
        print(f"  Ch{ch} ZH: {zh_by_ch[ch]}")
        print(f"       EN: {en_by_ch.get(ch, '(无)')}")
