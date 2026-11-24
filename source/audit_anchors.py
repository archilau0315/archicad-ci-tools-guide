"""清查所有 xref 链接是否都有对应的 h3 锚点。"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))

# 收集全站所有 h3 id（跨文件）
all_h3_ids = set()
for fname in os.listdir(SITE):
    if not fname.endswith(".html"): continue
    text = io.open(os.path.join(SITE, fname), encoding="utf-8").read()
    for i in re.findall(r'<h3\b[^>]*\sid="(s-[\d\-]+)"', text):
        all_h3_ids.add(i)

print(f"全站共有 {len(all_h3_ids)} 个 h3 锚点")

# 逐个文件查 xref href
broken = []
for fname in sorted(os.listdir(SITE)):
    if not fname.endswith(".html"): continue
    text = io.open(os.path.join(SITE, fname), encoding="utf-8").read()
    for m in re.finditer(r'<a[^>]*class="[^"]*xref[^"]*"[^>]*href="(#s-[\d\-]+)"', text):
        href = m.group(1)
        anchor = href.lstrip("#")
        if anchor not in all_h3_ids:
            broken.append((fname, anchor))

if broken:
    print(f"\n⚠️  共 {len(broken)} 个 xref 指向不存在的锚点：")
    for fname, anchor in broken:
        print(f"  {fname:40s} -> {anchor}")
else:
    print("✅ 全部 xref 锚点有效")

# 再反向查：有没有 h3 锚点完全没被任何 xref 引用（孤立锚点）
all_xref_hrefs = set()
for fname in os.listdir(SITE):
    if not fname.endswith(".html"): continue
    text = io.open(os.path.join(SITE, fname), encoding="utf-8").read()
    for m in re.finditer(r'<a[^>]*class="[^"]*xref[^"]*"[^>]*href="(#s-[\d\-]+)"', text):
        all_xref_hrefs.add(m.group(1).lstrip("#"))

orphan = all_h3_ids - all_xref_hrefs
print(f"\n未被任何 xref 引用的 h3 锚点：{len(orphan)} 个")
if orphan and len(orphan) <= 20:
    print("  " + ", ".join(sorted(orphan)[:20]))
elif orphan:
    print("  (数量较多，只显示前 15)")
    print("  " + ", ".join(sorted(orphan)[:15]))
