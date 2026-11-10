#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美化管线：md_to_html 基线 → 覆写 :root 主题 → 注入 webfont / 粘性目录 / 交互脚本
→ 补齐图片尺寸 → 质检

用法：
    python3 beautify.py manual_master.md manual.html
"""
import io, os, re, subprocess, sys, urllib.request, concurrent.futures as cf

SK = "C:/Users/user/AppData/Local/Programs/WorkBuddy/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/library"

CSS = """
:root {
  --accent: #2f6f8f; --accent2: #c9622a;
  --bg: #fbfbfa; --panel: #ffffff; --text: rgba(0,0,0,0.95);
  --muted: rgba(0,0,0,0.55); --line: rgba(0,0,0,0.10);
  --ink: #1c1c1a; --paper: #f3f2ee;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; color: var(--text); line-height: 1.72;
  font-family: "Noto Sans SC", -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 15px;
  background:
    radial-gradient(ellipse 70% 42% at 12% -8%, rgba(47,111,143,0.10), transparent),
    radial-gradient(ellipse 56% 44% at 88% 4%, rgba(201,98,42,0.07), transparent),
    var(--bg);
  background-attachment: fixed;
}
h1, h2, h3, h4 { font-family: "Noto Serif SC", Georgia, "Songti SC", serif; color: var(--ink); letter-spacing: -0.01em; }
h1 { font-size: clamp(30px, 5vw, 48px); font-weight: 700; line-height: 1.14; margin: 0 0 16px; }
h2 { font-size: clamp(22px, 3vw, 29px); font-weight: 700; line-height: 1.24; margin: 0 0 18px; padding-top: 8px; }
h3 { font-size: 17px; font-weight: 600; margin: 26px 0 10px; }
p { margin: 0 0 14px; }
a { color: var(--accent); text-decoration: none; border-bottom: 1px solid rgba(47,111,143,0.3); }
a:hover { border-bottom-color: var(--accent); }
strong { color: var(--ink); font-weight: 600; }
code { font-family: "Geist Mono", ui-monospace, "Cascadia Code", Consolas, monospace;
  font-size: 0.88em; background: rgba(47,111,143,0.08); padding: 2px 6px; border-radius: 4px;
  color: #1d4d63; font-variant-numeric: tabular-nums; }
ul, ol { margin: 0 0 16px; padding-left: 22px; }
li { margin-bottom: 7px; }
li::marker { color: var(--accent); }
blockquote {
  margin: 0 0 20px; padding: 14px 18px; background: var(--paper);
  border-left: 3px solid var(--accent); border-radius: 0 8px 8px 0; color: var(--muted);
}
blockquote p:last-child { margin-bottom: 0; }
.hero {
  max-width: 1080px; margin: 0 auto; padding: 88px 24px 56px;
  border-bottom: 1px solid var(--line);
}
.hero h1 { max-width: 17ch; }
.hero-summary { font-size: 17px; color: var(--muted); max-width: 62ch; margin: 0; line-height: 1.68; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 0 24px 96px; }
.block-card {
  background: var(--panel); border: 1px solid var(--line); border-radius: 12px;
  padding: 32px; margin: 0 0 24px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
}
.block-card > h2:first-child {
  padding-bottom: 14px; margin-bottom: 20px; border-bottom: 1px solid var(--line);
}
figure { margin: 22px 0; }
figure img {
  width: 100%; max-width: 100%; height: auto; display: block;
  border-radius: 8px; border: 1px solid var(--line); background: var(--paper);
}
figcaption { margin-top: 9px; font-size: 12.5px; color: var(--muted); line-height: 1.55; }
.table-wrap { overflow-x: auto; margin: 18px 0; border-radius: 8px; border: 1px solid var(--line); }
table { border-collapse: collapse; width: 100%; min-width: 460px; background: var(--panel); }
th, td { padding: 11px 14px; text-align: left; border-bottom: 1px solid var(--line); vertical-align: top; }
th { background: var(--paper); font-weight: 600; font-size: 13px; color: var(--ink); letter-spacing: 0.01em; }
tbody tr:last-child td { border-bottom: none; }
tbody tr:hover { background: rgba(47,111,143,0.035); }
hr { border: none; border-top: 1px solid var(--line); margin: 32px 0; }
.reveal { opacity: 0; transform: translateY(18px); transition: opacity 0.55s cubic-bezier(0.2,0,0,1), transform 0.55s cubic-bezier(0.2,0,0,1); }
.reveal.in { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) { .reveal { opacity: 1; transform: none; transition: none; } }
.toc { position: sticky; top: 0; z-index: 20; background: rgba(251,251,250,0.92);
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line); margin-bottom: 24px; }
.toc-inner { max-width: 1080px; margin: 0 auto; padding: 10px 24px;
  display: flex; align-items: center; gap: 14px; }
.toc-label { font-size: 12px; font-weight: 600; letter-spacing: 0.08em;
  color: var(--muted); text-transform: uppercase; flex-shrink: 0; }
.toc-list { list-style: none; display: flex; gap: 6px; margin: 0; padding: 0;
  overflow-x: auto; scrollbar-width: thin; flex: 1; }
.toc-list li { margin: 0; flex-shrink: 0; }
.toc-list a { display: inline-block; padding: 7px 12px; font-size: 13px; color: var(--muted);
  border: 1px solid transparent; border-radius: 9999px; white-space: nowrap;
  transition: background 0.2s, color 0.2s, border-color 0.2s; }
.toc-list a:hover { background: rgba(47,111,143,0.09); color: var(--accent);
  border-color: rgba(47,111,143,0.2); }
.toc-list a:active { transform: scale(0.97); }
.toc-toggle { display: none; border: 1px solid var(--line); background: var(--panel);
  color: var(--muted); font-size: 12px; padding: 7px 13px; border-radius: 9999px;
  cursor: pointer; font-family: inherit; min-height: 34px; }
h2 { scroll-margin-top: 78px; }
@media (max-width: 900px) {
  .toc-toggle { display: inline-block; }
  .toc-inner { flex-wrap: wrap; padding: 10px 16px; }
  .toc-list { width: 100%; display: none; padding-bottom: 6px; }
  .toc-list.open { display: flex; }
  h2 { scroll-margin-top: 104px; }
}
@media (max-width: 640px) {
  .hero { padding: 56px 18px 36px; }
  .wrap { padding: 0 16px 64px; }
  .block-card { padding: 20px; border-radius: 10px; }
  .block-card > h2:first-child { margin-bottom: 16px; }
  figure { margin: 18px 0; }
  .hero-summary { font-size: 15.5px; }
}
"""

FONTS = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/noto-serif-sc@5.3.0/chinese-simplified-700.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/geist-mono@5.2.5/index.css">
"""

JS = """
<script>
(function(){
  var btn = document.querySelector('.toc-toggle');
  var list = document.getElementById('toc-list');
  if (btn && list) {
    btn.addEventListener('click', function(){
      var open = list.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? '收起' : '展开全部';
    });
  }
  var links = document.querySelectorAll('.toc-list a');
  var secs = [];
  links.forEach(function(a){
    var el = document.querySelector(a.getAttribute('href'));
    if (el) secs.push({a:a, el:el});
  });
  if ('IntersectionObserver' in window && secs.length) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting) {
          secs.forEach(function(s){ s.a.style.color=''; s.a.style.borderColor=''; });
          var cur = secs.filter(function(s){ return s.el === e.target; })[0];
          if (cur) { cur.a.style.color = 'var(--accent)';
            cur.a.style.borderColor = 'rgba(47,111,143,0.28)'; }
        }
      });
    }, { rootMargin: '-80px 0px -70% 0px', threshold: 0 });
    secs.forEach(function(s){ io.observe(s.el); });
  }
})();
</script>
"""


def build(md_path, out_path, title):
    # 1) 基线
    tmp = out_path.replace(".html", "_base.html")
    r = subprocess.run(["python3", f"{SK}/page/md_to_html.py", "--md", md_path,
                        "--out", tmp, "--title", title, "--style", "tech", "--format", "page"],
                       capture_output=True, text=True)
    print(r.stdout.strip()[:200])
    h = io.open(tmp, encoding="utf-8").read()

    # 2) 覆写 :root 样式层
    i, j = h.find("<style>"), h.find("</style>")
    h = h[:i] + "<style>" + CSS + h[j:]

    # 3) webfont
    h = h.replace(f"<title>{title}</title>", f"<title>{title}</title>\n{FONTS}")

    # 4) 目录导航
    heads = re.findall(r"<h2>(.*?)</h2>", h)
    def slug(s):
        s = re.sub(r"<[^>]+>", "", s)
        return re.sub(r"[^\w\u4e00-\u9fa5]+", "-", s).strip("-")[:40]
    items = [(slug(t), re.sub(r"<[^>]+>", "", t)) for t in heads]
    nav = ['<nav class="toc" aria-label="目录"><div class="toc-inner"><span class="toc-label">目录</span>',
           '<button class="toc-toggle" aria-expanded="false" aria-controls="toc-list">展开全部</button>',
           '<ol class="toc-list" id="toc-list">']
    nav += [f'<li><a href="#{sid}">{txt}</a></li>' for sid, txt in items]
    nav.append("</ol></div></nav>")
    for (sid, _), t in zip(items, heads):
        h = h.replace(f"<h2>{t}</h2>", f'<h2 id="{sid}">{t}</h2>')
    h = h.replace('<main class="wrap">', "\n".join(nav) + "</main>")

    # 5) 交互脚本
    h = h.replace("</body>", JS + "</body>")

    # 6) 补图片尺寸
    urls = sorted(set(re.findall(r'<img[^>]+src="(https://[^"]+)"', h)))
    def get_size(u):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read()
            from PIL import Image
            return u, Image.open(io.BytesIO(data)).size
        except Exception:
            return u, None
    sizes = {}
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        for u, s in ex.map(get_size, urls):
            if s: sizes[u] = s
    def add_dims(mo):
        tag = mo.group(0)
        mu = re.search(r'src="([^"]+)"', tag)
        if not mu or mu.group(1) not in sizes or "width=" in tag: return tag
        w, hh = sizes[mu.group(1)]
        return tag.replace("<img ", f'<img width="{w}" height="{hh}" ')
    h = re.sub(r"<img[^>]+>", add_dims, h)

    io.open(out_path, "w", encoding="utf-8").write(h)
    os.remove(tmp)
    print(f"章节 {len(items)}｜图片 {len(urls)}（带尺寸 {len(sizes)}）｜输出 {out_path}")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "Archicad CI Tools 完整用户手册")
